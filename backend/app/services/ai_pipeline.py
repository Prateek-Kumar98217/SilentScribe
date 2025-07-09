from sqlalchemy.orm import Session
from app.repositories.codefile import get_codefile
from app.repositories.codeblock import delete_blocks_by_file, create_codeblocks_bulk
from app.repositories.codereview import create_review
from app.repositories.codereview import get_review_by_block
from app.repositories.refactor import create_refactored_code
from app.repositories.codetest import create_test
from app.repositories.narration import create_narration

def run_ai_pipeline_for_codefile(codefile_id: str, db: Session):
    codefile=get_codefile(db, codefile_id)
    if not codefile:
        raise Exception("Codefile not found")
    
    delete_blocks_by_file(db, codefile_id)

    parsed_blocks=run_parsing_chain(codefile.content)
    for block in parsed_blocks:
        block["file_id"]=codefile.id
    code_blocks=create_codeblocks_bulk(db, parsed_blocks)

    for block in code_blocks:
        review_result=run_review_chain(block.code)
        create_review(db, block.id, review_result)

    for block in code_blocks:
        review=get_review_by_block(db, block.id)
        if review.requires_refactor:
            refactor_result=run_refactor_chain(block.code)
            refactor_result["block_id"]=block.id
            refactor=create_refactored_code(db, refactor_result)
            refactor_narration=run_narration_chain(refactor.refactored_code, target="refactored")
            refactor_narration["refactored_id"]=refactor.id
            create_narration(db, refactor_narration)


    for block in code_blocks:
        test=run_test_gen_chain(block.code)
        test["block_id"]=block.id
        test_block=create_test(db, test)
        test_narration=run_narration_chain(test.test_code, target="test")
        test_narration["test_id"]=test_block.id
        refactor_narration=run_narration_chain(test_block.refactored_code, target="refactored")
        create_narration(db, refactor_narration)

            
def run_parsing_chain(content: str):
    pass

def run_review_chain():
    pass

def run_refactor_chain():
    pass

def run_test_gen_chain():
    pass

def run_narration_chain():
    pass