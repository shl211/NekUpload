from pathlib import Path
import h5py
from typing import Union, Dict, Any, Tuple, Optional, List
import numpy as np
import xml.etree.ElementTree as ET
import re

def get_absolute_path(path: str) -> str:
    path_obj = Path(path)
    abs_path = path_obj.resolve()
    return str(abs_path)

def print_hdf5_file_structure(file_path: str) -> None:
    file_abs_path = get_absolute_path(file_path)
    
    with h5py.File(file_abs_path, 'r') as hdf_file:
        print("HDF5 File Structure:")
        hdf_file.visititems(_print_hdf5_structure_msg)

def inspect_hdf5_key(file_path: str, key: str) -> Dict[str, Any]:
    result = {}
    file_abs_path = get_absolute_path(file_path)

    with h5py.File(file_abs_path, 'r') as hdf_file:
        
        try:
            obj = hdf_file[key]
        except KeyError:
            raise KeyError(f"Key '{key}' not found in the HDF5 file.")
            
        result["attributes"] = dict(obj.attrs)

        if isinstance(obj, h5py.Group):
            result["type"] = "Group"
            result["contents"] = list(obj.keys())
        elif isinstance(obj, h5py.Dataset):
            result["type"] = "Dataset"
            # Snippet of data (first 10 elements if it's a 1D array, otherwise shape)
            if obj.ndim == 1:
                result["contents"] = {"shape": obj.shape, "snippet": obj[:10].tolist()}  # Convert to list for readability
            else:
                result["contents"] = {"shape": obj.shape, "snippet": obj[:2, :].tolist()}
        else: 
            result["type"] = "Unkown"
            result["contents"] = None
        
    return result

def hdf5_to_plain_text(input_file: str, output_file: str) -> None:
    input_file = get_absolute_path(input_file)
    output_file = get_absolute_path(output_file)

    with h5py.File(input_file, 'r') as hdf:
        # Process the root group
        output_lines = _print_hdf5_group(hdf)
    
    # Write the collected lines to the output text file
    with open(output_file, 'w') as f:
        f.write("\n".join(output_lines))
    
    print(f"HDF5 file content has been written to {output_file} in plain text format.")

def read_dataset_from_hdf5_file(file_path: str, dataset_name: str, start: Optional[Tuple]=None, chunk_size: Optional[Tuple]=None) -> np.ndarray:
    """Reads a dataset, optionally in chunks, and returns the dataset

    Args:
        file_path (str): Path to hdf5 file
        dataset_name (str): Dataset name
        start (Optional[Tuple], optional): Start index of array to be read. Defaults to None.
        chunk_size (Optional[Tuple], optional): Number of elements of array to be read in each dimension. Defaults to None.

    Returns:
        np.ndarray: Array of data stored in dataset
    """
    file_path = get_absolute_path(file_path)

    with h5py.File(file_path, 'r') as hdf_file:
        dataset = hdf_file[dataset_name]

        if start is None or chunk_size is None:
            data_chunk = dataset[:]
        else:
            if len(start) != len(dataset.shape):
                raise ValueError("Start dimensions must match the dataset dimensions.")
            if len(chunk_size) != len(dataset.shape):
                raise ValueError("Chunk size dimensions must match the dataset dimensions.")

            for i, (s, c, max_dim) in enumerate(zip(start, chunk_size, dataset.shape)):
                if s < 0 or s >= max_dim:
                    raise ValueError(f"Start index {s} for dimension {i} is out of bounds.")
                if s + c > max_dim:
                    raise ValueError(f"Chunk size {c} for dimension {i} exceeds bounds.")

            slices = tuple(slice(s,s+c) for s,c in zip(start,chunk_size))
            data_chunk = dataset[slices]

    return data_chunk

def read_attributes_from_hdf5_file(file_path: str, group_name: str) -> Dict[str, Any]:
    attributes: Dict[str, Any] = {}
    try:
        with h5py.File(file_path, 'r') as hdf_file:
            if group_name not in hdf_file:
                raise KeyError(f"Group '{group_name}' does not exist in the file.")
            
            group = hdf_file[group_name]
            attributes = {key: value for key, value in group.attrs.items()}
    
    except Exception as e:
        print(f"Error reading attributes: {e}")
    
    return attributes

def print_XML_file_structure(xml_file: str, indent: int = 2) -> None:
    xml_file = get_absolute_path(xml_file)
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        _print_XML_element(root, indent)
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
    except FileNotFoundError:
        print(f"File not found: {xml_file}")

def read_xml_tag_contents(xml_file: str, tag: str) -> Optional[Dict[str, Any]]:
    xml_file = get_absolute_path(xml_file)
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # First, check if the root element matches the tag
        if root.tag == tag:
            return [{
                "attributes": root.attrib,
                "content": root.text.strip() if root.text else ""
            }]
        
        # Find all other occurrences of the tag
        elements = root.findall(f".//{tag}")
        
        if not elements:
            print(f"Tag '{tag}' not found.")
            return None
        
        result = []
        for element in elements:
            # Get the tag's attributes as a dictionary
            attributes = element.attrib
            
            # Get the tag's text content (if any)
            content = element.text.strip() if element.text else ""
            
            result.append({
                "attributes": attributes,
                "content": content
            })
        
        return result
    
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return None
    except FileNotFoundError:
        print(f"File not found: {xml_file}")
        return None

def extract_all_tag_content(xml_file: str, tag: str) -> str:
    """
    Extracts the raw XML content between a specified tag.
    
    Args:
        xml_file (str): Path to the XML file.
        tag (str): The tag name whose content to extract.
    
    Returns:
        str: The raw XML content between the specified tag, or an empty string if the tag is not found.
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Find the first occurrence of the tag
        element = root.find(f".//{tag}")
        
        if element is None:
            print(f"Tag '{tag}' not found.")
            return ""
        
        # Use ET.tostring to get the raw content including nested tags
        from xml.etree.ElementTree import tostring
        content = tostring(element, encoding="unicode")
        
        return content
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return ""

def extract_self_closing_tags(raw_string: str, tag: str) -> List:        
    # Use regex to find all occurrences of self-closing tags
    pattern = rf"<{tag}\s[^>]*?/>"  # Matches <E ... />
    matches = re.findall(pattern, raw_string)
    return matches

def parse_attributes(tag_string: str) -> dict:
    # Remove the tag name and self-closing brackets
    attributes_part = re.search(r"<E\s(.*?)/>", tag_string).group(1)
    # Split into key-value pairs
    attributes = re.findall(r'(\w+)="(.*?)"', attributes_part)
    return dict(attributes)

def insert_and_merge_intervals(intervals: List[List[float]], new_interval: List[float]) -> List[List[float]]:
    result = []
    inserted = False

    for interval in intervals:
        if interval[1] < new_interval[0] - 1:  # Interval ends before new_interval starts
            result.append(interval)
        elif interval[0] > new_interval[1] + 1:  # Interval starts after new_interval ends
            if not inserted:
                result.append(new_interval)  # Insert the new interval
                inserted = True
            result.append(interval)
        else:  # Overlapping intervals, merge them
            new_interval = [min(new_interval[0], interval[0]), max(new_interval[1], interval[1])]

    if not inserted:
        result.append(new_interval)  # Add the new interval if not yet added

    return result

def count_num_in_interval(intervals: List[List[float]]) -> int:
    if type(intervals) == int or type(intervals) == None:
        return 0
    
    count = 0
    for interval in intervals:
        count += interval[1] - interval[0] + 1

    return count

def is_in_interval(num: int, intervals: List[List[float]]) -> bool:
    #currently O(n) linear search, can improve to O(logn) binary search
    for interval in intervals:
        start = interval[0]
        end = interval[1]

        if start <= num and num <= end:
            return True
        elif num < start:
            return False
    
    return False

def is_interval_in_interval(interval1: List[float], interval_list: List[List[float]]) -> bool:
    #currently O(n) brute force, can improve to O(logn) with binary search, also can early terminate 
    start = interval1[0]
    end = interval1[1]

    for interval in interval_list:
        int_start = interval[0]
        int_end = interval[1]
        if start >= int_start and end <= int_end:
            return True

    return False

#def convert_mixed_list_to_range

def _print_hdf5_group(group: h5py.Group, indent: int=0) -> List[str]:
        """
        Recursively process an HDF5 group and return its content as a string.
        """
        lines = []
        indent_str = "    " * indent

        # Print group attributes
        lines.append(f"{indent_str}Group: {group.name}")
        if group.attrs:
            lines.append(f"{indent_str}  Attributes:")
            for key, value in group.attrs.items():
                lines.append(f"{indent_str}    {key}: {value}")

        # Iterate through items in the group
        for name, item in group.items():
            if isinstance(item, h5py.Group):
                # Recurse into subgroups
                lines.extend(_print_hdf5_group(item, indent + 1))
            elif isinstance(item, h5py.Dataset):
                # Print dataset attributes and data
                lines.append(f"{indent_str}  Dataset: {name}")
                if item.attrs:
                    lines.append(f"{indent_str}    Attributes:")
                    for key, value in item.attrs.items():
                        lines.append(f"{indent_str}      {key}: {value}")
                lines.append(f"{indent_str}    Shape: {item.shape}")
                lines.append(f"{indent_str}    Dtype: {item.dtype}")
                lines.append(f"{indent_str}    Data: {item[...]}")

        return lines

def _print_XML_element(element: ET.Element, indent: int=2, level: int=0) -> None:
        indent_space = ' ' * (level * indent)
        attr_str = ', '.join(f'{k}="{v}"' for k, v in element.attrib.items())
        print(f"{indent_space}<{element.tag} {attr_str}>".strip())
        
        for child in element:
            _print_XML_element(child, level + 1)

        print(f"{indent_space}</{element.tag}>".strip())

def _print_hdf5_structure_msg(name: str, obj: Union[h5py.Group,h5py.Dataset]) -> None:
    obj_type = "Group" if isinstance(obj, h5py.Group) else "Dataset"
    print(f"{name} ({obj_type})")