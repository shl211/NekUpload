import click
from NekUpload.uploadModule import invenioRDM
from NekUpload.metadataModule import *
from NekUpload.metadataModule.user import UserInfo
from typing import Dict,List,Tuple,Any
from dataclasses import dataclass,field
from datetime import date
import json
import os
import pathlib
import yaml

@dataclass
class Config:
    #use field to ensure independent instances of authors
    authors: List[InvenioOrgInfo | InvenioPersonInfo] = field(default_factory=list)
    metadata: InvenioMetadata = None

    CONTEXT_FILE: pathlib.Path = "config.json"

    def to_json(self):
        data = {
            "CONTEXT_FILE": str(self.CONTEXT_FILE)
        }
        
        #only jsonify non empty data
        if self.metadata:
            data["metadata"] = self.metadata.to_json_serialisable()
        
        if self.authors:
            data["authors"] = [author.to_json_serialisable() for author in self.authors]

        return data
    
    @classmethod
    def from_json(cls,data: Dict[str,Any]) -> 'Config':
        config = Config()
        
        config.CONTEXT_FILE = pathlib.Path(data["CONTEXT_FILE"])

        if metadata := data.get("metadata",None):
            config.metadata = InvenioMetadata.from_json(metadata)

        if authors := data.get("authors",[]):
            config.authors = [UserInfo.from_json(author) for author in authors]

        return config

    @staticmethod
    def yaml_quickstart():
        
        
        
        pass

    @classmethod
    def from_yaml(cls,data: Dict[str,Any]) -> 'Config':
        metadata: Dict[str,Any] = data["metadata"]
        title = metadata["title"]
        publication_date = metadata["publication_date"]
        description = metadata.get("description",None)
        publisher = metadata.get("publisher","NekUpload-CLI")
        authors: List[Dict[str,Any]] = metadata["authors"] 

        def get_authors(yaml_data: Dict[str,Any]) -> UserInfo:
            """Turn yaml representation of authors into json"""
            json = yaml_data

            identifiers = json.get("identifiers",[])

            identifier = None
            if identifiers:
                #if identifiers have been specified, remove it from json
                #redefine it
                json.pop("identifiers")
                
                #right now, only orcid is supported
                orcid = identifiers.get("orcid")
                if orcid:
                    identifier = Identifier(orcid,IdentifierType.ORCID)

            #define author
            author = UserInfo.from_json(json)

            if identifier:
                author.add_identifier(identifier)
            return author

        author_list = [get_authors(author) for author in authors]

        config = Config()
        config.authors = author_list
        metadata_obj = InvenioMetadata(title,publication_date,author_list)        
        metadata_obj.add_publisher(publisher)

        if description:
            #currently no support for description, but will change in future
            pass

        config.metadata = metadata_obj
        return config

@click.group()
@click.option("--config","-c",type=click.Path(dir_okay=False, path_type=pathlib.Path),default="config.json",help="Use specified config file, defaults to config.json")
@click.pass_context
def cli(ctx: click.Context, config: pathlib.Path):
    ctx.ensure_object(Config)
    try:
        with open(config,"r") as f:
            ctx.obj = Config.from_json(json.load(f))
    except FileNotFoundError:
        ctx.obj = Config()
    except json.JSONDecodeError:
        click.echo(f"Warning: Could not parse {config}. Starting with a fresh config.")
        ctx.obj = Config()

    ctx.obj.CONTEXT_FILE = config
    ctx.call_on_close(lambda: save_config(ctx,config))

def save_config(ctx: click.Context,config_file: pathlib.Path):
    with open(config_file, "w") as f:
        json.dump(ctx.obj.to_json(), f, indent=4)
    click.echo(f"Config saved to {config_file}")

@cli.command()
@click.argument('given_name')
@click.argument('last_name')
@click.option('--orcid',help="orcid identifier")
@click.option('--affiliation',help="affiliated with what organisation")
@click.pass_context
def add_author_person(ctx: click.Context,given_name: str,last_name: str,orcid: str=None,affiliation: str=None):
    """Add an author, who is a person

    \b
    GIVEN_NAME: Given name of author (use quotes if there is a space)
    LAST_NAME: Last name of author (use quotes if there is a space)
    """
    author = InvenioPersonInfo(given_name,last_name)

    if orcid:
        author.add_identifier(Identifier(orcid,IdentifierType.ORCID))

    config: Config = ctx.obj
    config.authors.append(author)

@cli.command()
@click.argument('name')
@click.option('--orcid',help="orcid identifier")
@click.option('--affiliation',help="affiliated with what organisation")
@click.pass_context
def add_author_org(ctx: click.Context,name: str,orcid: str=None,affiliation: str=None):
    """Add an author, who is a organisation

    \b
    NAME: Name of organisation (use quotes if there is a space)
    LAST_NAME: Last name of author (use quotes if there is a space)
    """
    author = InvenioOrgInfo(name)

    if orcid:
        author.add_identifier(Identifier(orcid,IdentifierType.ORCID))

    config: Config = ctx.obj
    config.authors.append(author)

@cli.command()
@click.argument("title")
@click.option("--pub-date",help="Publication date, defaults to today's date")
@click.pass_context
def add_info(ctx: click.Context,title: str,pub_date: str=None):
    """Add information about datasets to be uploaded

        \b
        TITLE: dataset title
    """
    config: Config = ctx.obj

    if not pub_date:
        today: date = date.today() 
        pub_date = today.isoformat()

    metadata = InvenioMetadata(title,pub_date,config.authors,"dataset")
    config.metadata = metadata

@cli.command()
@click.option('-u',"--user-config",help="user-defined yaml file containing upload settings")
@click.option("--api-key", envvar="NEKTAR_DB_API_KEY", help="Your API key (or set environment variable NEKTAR_DB_API_KEY)")
@click.option("--host", envvar="NEKTAR_DB_HOST", help="Host name of database (or set environment variable NEKTAR_DB_HOST)")
@click.option("--community-slug", envvar="NEKTAR_DB_COMMUNITY", help="Community id to upload to (or set environment variable NEKTAR_DB_COMMUNITY)")
@click.option("-dir","--directory",type=click.Path(exists=True), help="Directory containing files to be uploaded")
@click.option('-f', '--file', multiple=True, type=click.Path(exists=True), help="Path to a file to be uploaded, can specify multiple e.g. -f file1 -f file2")
@click.pass_context
def upload(ctx: click.Context,api_key: str=None, host: str=None, community_slug: str=None,directory: str=None,file:Tuple[str]=None,user_config:str=None):
    """Validate and upload the files to the specified database
    """

    #for this, all data is assumed to be within the user config file
    if user_config:
        upload_user_config(user_config)
        return

    if not api_key:
        click.echo("Error: API key is required. Set the NEKTAR_DB_API_KEY environment variable or use the --api-key option.")
        return
    
    if not host:
        click.echo("Error: Host name is required. Set the NEKTAR_DB_HOST environment variable or use the --host option")
        return

    if not community_slug:
        click.echo("Error: Community id is required. Set the NEKTAR_DB_COMMUNITY environment variable or use the --community-slug option")
        return 
    
    if not directory and not file:
        click.echo("Error: No files detected. Set files either via -f or the directory via -dir") 

    files = None
    if directory:
        files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    elif file:
        files = [f for f in file]
    
    config: Config = ctx.obj
    
    if not config.metadata:
        click.echo("Error: No metadata set. Please use the command add_info")
        return 
    
    if config.authors == []:
        click.echo("Error: No authors set. Please set an author with command add_author_person or add_author_org")
        return 
    
    db = invenioRDM()
    metadata = {"metadata": config.metadata.get_metadata_payload()}
    db.upload_files(host,api_key,files,metadata,community_slug)

def upload_user_config(user_config_file: str):
    yaml: Dict[str,Any] = read_yaml_file(user_config_file)
    config = Config.from_yaml(yaml)

    db = yaml["database"]
    host_name = db["host_name"]
    #unsafe key storage atm
    api_key = db["api_key"]
    community_slug = db["community_slug"]

    upload_data = yaml["upload"]
    upload_files = upload_data.get("files",[])
    upload_dirs = upload_data.get("directories",[])

    #collect all files specified in directory
    if upload_dirs:
        for dir in upload_dirs:
            files = [os.path.join(dir, f) for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
            upload_files.append(files)

    db = invenioRDM()
    metadata = {"metadata": config.metadata.get_metadata_payload()}
    
    db.upload_files(host_name,api_key,upload_files,metadata,community_slug)


@cli.command()
@click.pass_context
def list_authors(ctx: click.Context):
    """List all authors."""
    config: Config = ctx.obj
    for author in config.authors:
        click.echo(author)

def read_yaml_file(filepath):
    """Reads a YAML file and returns the parsed data.

    Args:
        filepath: The path to the YAML file.

    Returns:
        The parsed YAML data as a Python object (usually a dictionary or list),
        or None if an error occurs (e.g., file not found, invalid YAML).
    """
    try:
        with open(filepath, 'r') as file:
            yaml_data = yaml.safe_load(file)  # Use safe_load to avoid potential security issues
            return yaml_data
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return None


def main():#Entry point
    cli()

if __name__ == "__main__":
    main()