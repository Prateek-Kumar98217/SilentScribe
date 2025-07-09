import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()


def gen_uuid():
    return str(uuid.uuid4())


class CodeTypeEnum(str, enum.Enum):
    function = "function"
    class_ = "class"
    module = "module"
    import_ = "import"
    variable = "variable"


class NarrationTargetEnum(str, enum.Enum):
    block = "block"
    refactored = "refactored"
    test = "test"


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=gen_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    projects = relationship("Project", back_populates="owner", cascade="all, delete")


class Project(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True, default=gen_uuid)
    title = Column(String, index=True, nullable=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="projects")
    codefiles = relationship("CodeFile", back_populates="project", cascade="all, delete")


class CodeFile(Base):
    __tablename__ = "codefiles"
    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    project_id = Column(String, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="codefiles")
    codeblocks = relationship("CodeBlock", back_populates="codefile", cascade="all, delete")


class CodeBlock(Base):
    __tablename__ = "codeblocks"
    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String, index=True)
    code_type = Column(Enum(CodeTypeEnum), nullable=False)
    docstring = Column(String, nullable=True)
    code = Column(Text, nullable=False)

    file_id = Column(String, ForeignKey("codefiles.id"), nullable=False)
    codefile = relationship("CodeFile", back_populates="codeblocks")

    review = relationship("CodeReview", uselist=False, back_populates="block", cascade="all, delete")
    refactored = relationship("RefactoredCode", uselist=False, back_populates="block", cascade="all, delete")
    test = relationship("GeneratedTest", uselist=False, back_populates="block", cascade="all, delete")
    narrations = relationship("Narration", back_populates="block", cascade="all, delete")


class CodeReview(Base):
    __tablename__ = "code_reviews"
    id = Column(String, primary_key=True, default=gen_uuid)
    issues = Column(Text)
    quality_score = Column(Float, nullable=False)
    requires_refactor = Column(Boolean, default=False)
    comments = Column(Text)

    block_id = Column(String, ForeignKey("codeblocks.id", ondelete="CASCADE"))
    block = relationship("CodeBlock", back_populates="review")


class RefactoredCode(Base):
    __tablename__ = "refactored_code"
    id = Column(String, primary_key=True, default=gen_uuid)
    refactored_code = Column(Text, nullable=False)
    change_summary = Column(Text)

    block_id = Column(String, ForeignKey("codeblocks.id", ondelete="CASCADE"))
    block = relationship("CodeBlock", back_populates="refactored")
    narrations = relationship("Narration", back_populates="refactored", cascade="all, delete")


class GeneratedTest(Base):
    __tablename__ = "generated_tests"
    id = Column(String, primary_key=True, default=gen_uuid)
    test_code = Column(Text, nullable=False)
    coverage_summary = Column(Text)

    block_id = Column(String, ForeignKey("codeblocks.id", ondelete="CASCADE"))
    block = relationship("CodeBlock", back_populates="test")
    narrations = relationship("Narration", back_populates="test", cascade="all, delete")


class Narration(Base):
    __tablename__ = "narrations"
    id = Column(String, primary_key=True, default=gen_uuid)
    target_type = Column(Enum(NarrationTargetEnum))
    content = Column(Text)
    style = Column(String, nullable=True)

    block_id = Column(String, ForeignKey("codeblocks.id", ondelete="CASCADE"), nullable=True)
    test_id = Column(String, ForeignKey("generated_tests.id", ondelete="CASCADE"), nullable=True)
    refactored_id = Column(String, ForeignKey("refactored_code.id", ondelete="CASCADE"), nullable=True)

    block = relationship("CodeBlock", back_populates="narrations")
    test = relationship("GeneratedTest", back_populates="narrations")
    refactored = relationship("RefactoredCode", back_populates="narrations")
