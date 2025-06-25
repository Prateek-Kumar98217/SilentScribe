from app.models import CodeBlock, CodeFile
from app.services import parsing
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def get_all_codeblocks(db: Session, file_id: int) -> list[CodeBlock]:
    """
    Retrieve all code blocks of a code file from the database.
    """
    codeblocks = db.query(CodeBlock).filter(CodeBlock.file_id == file_id).all()
    if not codeblocks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No code blocks from the code file{file_id} found"
        )
    return codeblocks

def get_codeblock(db: Session, codeblock_id: int)-> CodeBlock:
    """
    Retrieve a code block by its ID.
    """
    codeblock = db.get(CodeBlock, codeblock_id)
    if not codeblock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Code block with ID {codeblock_id} not found"
        )
    return codeblock

def get_codeblock_by_name(db: Session, file_id: int, block_name: str)->CodeBlock:
    """
    Retrieve a code block by its name within a specific code file.
    """
    codeblock=db.query(CodeBlock).filter(
        CodeBlock.file_id == file_id,
        CodeBlock.name == block_name
    ).first()
    if not codeblock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Code block with name {block_name} not found in code file {file_id}"
        )
    return codeblock

def initialize_codeblocks(db:Session, file_id: int) -> list[CodeBlock]:
    """
    Create code blocks for the file in the database if they dont exist for the file
    """
    codeblocks = db.query(CodeBlock).filter(CodeBlock.file_id == file_id).all()
    if codeblocks:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Code blocks already exist for code file with ID {file_id}"
        )
    return _parse_and_create_codeblocks(db, file_id)
    

def refresh_codeblocks(db: Session, file_id: int) -> list[CodeBlock]:
    """
    Reparse the code blockes of a file and update the database
    """
    db.query(CodeBlock).filter(CodeBlock.file_id == file_id).delete(synchronize_session=False)
    db.commit()
    return _parse_and_create_codeblocks(db, file_id)

def delete_codeblocks_by_file_id(db:Session, file_id: int)-> None:
    """
    Delete all the code blocks for a given file ID from the database
    """
    db.query(CodeBlock).filter(CodeBlock.file_id == file_id).delete(synchronize_session=False)
    db.commit()
    return None

#helper function for parsing and creating code blocks
def _parse_and_create_codeblocks(db: Session, file_id: int) -> list[CodeBlock]:
    file = db.get(CodeFile, file_id)
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Code file with ID {file_id} not found"
        )
    codeblocks = parsing.parse_file_to_blocks(file.file_content)
    if not codeblocks:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No code blocks found in the file content"
        )
    codeblock_objects = []
    for block in codeblocks:
        codeblock = CodeBlock(
            code_type=block["type"],
            name=block["name"],
            lineno=block["lineno"],
            col_offset=block["col_offset"],
            end_lineno=block["end_lineno"],
            end_col_offset=block["end_col_offset"],
            docstring=block["docstring"],
            used_names=block["used_names"],
            args=block["args"],
            returns=block["returns"],
            code=block["code"],
            file_id=file_id
        )
        db.add(codeblock)
        codeblock_objects.append(codeblock)
    db.commit()
    for codeblock in codeblock_objects:
        db.refresh(codeblock)
    return codeblock_objects