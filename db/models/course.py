from datetime import datetime
import enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from ..db_setup import Base
from .user import User
from .mixins import Timestamp


class ContentType(enum.Enum):
    lesson = 1
    quiz = 2
    assignment = 3


class Course(Timestamp, Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_by = relationship(User)
    sections = relationship("Section", back_populates="course", uselist=False)
    student_courses = relationship("StudentCourse", back_populates="course")


class Section(Timestamp, Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    course = relationship("Course", back_populates="sections")


class ContentBlock(Timestamp, Base):
    __tablename__ = "content_blocks"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(Enum(ContentType))
    url = Column(URLType, nullable=True)
    content = Column(Text, nullable=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)

    section = relationship("Section", back_populates="content_blocks")


class StudentCourse(Timestamp, Base):
    __tablename__ = "student_courses"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    completed = Column(Boolean, default=False)

    student = relationship(User, back_populates="student_courses")
    course = relationship("Course", back_populates="student_courses")


class CompletedContentBlock(Timestamp, Base):
    __tablename__ = "completed_content_blocks"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_block_id = Column(Integer, ForeignKey(
        "content_blocks.id"), nullable=False)
    url = Column(URLType, nullable=True)
    feedback = Column(Text, nullable=True)
    grade = Column(Integer, default=0)

    student = relationship(User, back_populates="student_content_blocks")
    content_block = relationship(
        ContentBlock, back_populates="completed_content_blocks")
