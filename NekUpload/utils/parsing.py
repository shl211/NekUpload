from typing import Tuple,Dict,Union,List,Optional
import math
import h5py
from sympy import sympify

#these are as defined in Nektar User Guide under Expressions
#https://doc.nektar.info/userguide/latest/user-guidese13.html
MATH_CONSTANTS: Dict[str,float] = {
    "E": math.e,
    "PI": math.pi,
    "GAMMA": 0.57721566490153286060,
    "DEG": 180 / math.pi,  # Degrees per radian
    "PHI": (1 + math.sqrt(5)) / 2,  # Golden ratio
    "LOG2E": math.log2(math.e),
    "LOG10E": math.log10(math.e),
    "LN2": math.log(2),
    "PI_2": math.pi / 2,
    "PI_4": math.pi / 4,
    "1_PI": 1 / math.pi,
    "2_PI": 2 / math.pi,
    "2_SQRTPI": 2 / math.sqrt(math.pi),
    "SQRT2": math.sqrt(2),
    "SQRT1_2": math.sqrt(0.5),
}

def get_both_sides_of_equals(text_with_equals: str) -> Tuple[str, str]:
    """Given a strting "LHS = RHS", acquire LHS and RHS

    Args:
        text_with_equals (str): _description_

    Returns:
        Tuple[str, str]: _description_
    """
    left, right = text_with_equals.split("=")
    return left.strip(), right.strip()

def safe_resolve(param_name: str, params: Dict[str, str], seen: set) -> Union[float, str]:
    """
    Recursively resolves and evaluates expressions in params.
    
    Args:
        param_name (str): The name of the parameter to resolve.
        params (Dict[str, str]): Dictionary of parameters mapping names to expressions.
        seen (set): Set of already visited parameters (to prevent cycles).
    
    Returns:
        Union[float, str]: Evaluated numerical result or original string if resolution fails.
    """
    if param_name in seen:
        raise ValueError(f"Circular reference detected: {' -> '.join(seen)} -> {param_name}")

    seen.add(param_name)  # Track visited parameters
    
    # Get the value (expression) of the parameter
    expr = params.get(param_name, param_name)  # Default to itself if not found
    
    # Try converting to number directly
    try:
        return float(expr)
    except ValueError:
        pass  # Not a direct number, so evaluate it

    # Replace references to other parameters
    for key in params:
        if key in expr:
            resolved_value = safe_resolve(key, params, seen.copy())  # Recursively resolve
            expr = expr.replace(key, str(resolved_value))

    # Evaluate safely using sympy
    try:
        return float(sympify(expr, locals=MATH_CONSTANTS))
    except Exception:
        return expr  # Return as string if evaluation fails

def evaluate_parameters(params: Dict[str, str]) -> Dict[str, float]:
    """
    Evaluates all parameters in a dictionary.

    Args:
        params (Dict[str, str]): Dictionary mapping parameter names to expressions.
    
    Returns:
        Dict[str, float]: Evaluated parameters with numerical values.
    """
    evaluated = {}
    for param in params:
        evaluated[param] = safe_resolve(param, params, set())
    return evaluated

def get_all_files_with_extension(files: List[str],extension: str) -> List[str]:
    """Return all files in a list with the specified file extension

    Args:
        files (List[str]): _description_
        extension (str): _description_

    Returns:
        List[str]: _description_
    """
    # Ensure extension starts with "."
    if not extension.startswith("."):
        extension = f".{extension}"
    
    return [f for f in files if f.lower().endswith(extension.lower())]

def get_hdf5_groups_with_depth_limit(hdf5_file: h5py.File,max_depth: int,start_path: str = "",max_groups: int = 100) -> List[str]:
    """
    Traverses the HDF5 hierarchy and returns group paths up to a specified depth.

    Args:
        hdf5_file: An open h5py.File object.
        max_depth: The maximum depth to traverse.
        start_path: the path to start the search from.
        max_groups: If defined, specifies maximum number of groups to be found. Once exceeded, function will return.

    Returns:
        A list of group paths.
    """
    group_paths = []

    def _traverse(group, current_path, current_depth):
        if current_depth > max_depth:
            return

        if len(group_paths) >= max_groups:
            return
        
        group_paths.append(current_path)

        for name, obj in group.items():
            if isinstance(obj, h5py.Group):
                new_path = f"{current_path}/{name}" if current_path else name
                _traverse(obj, new_path, current_depth + 1)

    if start_path == "":
        _traverse(hdf5_file, "", 0)
    else:
        _traverse(hdf5_file[start_path], start_path, 0)

    return group_paths

def get_hdf5_datasets_with_depth_limit(hdf5_file: h5py.File,max_depth: int,start_path: str = "",max_datasets: int=100) -> List[str]:
    """Traverses the HDF5 hierarchy and returns dataset paths up to a specified depth.

    Args:
        hdf5_file: An open h5py.File object.
        max_depth: The maximum depth to traverse.
        start_path: The path to start the search from.
        max_datasets: If defined, specifies maximum number of datasets to be found. Once exceeded, function will return.

    Returns:
        A list of dataset paths.
    """
    dataset_paths = []

    def _traverse(group, current_path, current_depth):
        if current_depth > max_depth:
            return

        for name, obj in group.items():
            if len(dataset_paths) >= max_datasets:
                return
            new_path = f"{current_path}/{name}" if current_path else name
            if isinstance(obj, h5py.Dataset):
                dataset_paths.append(new_path)
            elif isinstance(obj, h5py.Group):
                _traverse(obj, new_path, current_depth + 1)

    if start_path == "":
        _traverse(hdf5_file, "", 0)
    else:
        _traverse(hdf5_file[start_path], start_path, 0)

    return dataset_paths

if __name__ == "__main__":
    params = {
        "A": "2",
        "NEK": "A + PI_2",
        "C": "NEK*2"
    }

    print(evaluate_parameters(params))

