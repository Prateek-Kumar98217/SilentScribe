from pydantic import BaseModel
from typing import List, Optional, Literal


class CodeBlockAI(BaseModel):
    code_type: Literal["function", "class", "module", "import", "variable"]
    name: Optional[str]
    docstring: Optional[str]
    code: str


class CodeBlockResponseList(BaseModel):
    __root__: List[CodeBlockAI]


class CodeParseInput(BaseModel):
    code: str


class CodeReviewAIInput(BaseModel):
    block_name: Optional[str]
    code: str


class CodeReviewAIOutput(BaseModel):
    quality_score: float
    requires_refactor: bool
    issues: List[str]
    comments: Optional[str]


class RefactorAIInput(BaseModel):
    code: str
    known_issues: Optional[List[str]] = None


class RefactorAIOutput(BaseModel):
    refactored_code: str
    change_summary: Optional[str]


class TestGenAIInput(BaseModel):
    code: str
    function_name: Optional[str]


class TestGenAIOutput(BaseModel):
    test_code: str
    coverage_summary: Optional[str]


class NarrationAIInput(BaseModel):
    target_type: Literal["block", "test", "refactored"]
    code: str
    style: Optional[str] = "educational"


class NarrationAIOutput(BaseModel):
    content: str
