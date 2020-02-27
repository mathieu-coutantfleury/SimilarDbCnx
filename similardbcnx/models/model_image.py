# -*- coding: utf-8 -*-
__author__ = 'Mathieu COUTANT FLEURY'
"""File to define model of DB"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Table
from similardbcnx.models import BaseImage
from sqlalchemy.orm import relationship


# table d'association entre une operation SE et un objectif
LnkImageExifData = Table('lnk_image_exifdata', BaseImage.metadata,
                         Column('id_image', Integer, ForeignKey('images.id')),
                         Column('id_exifdata', Integer, ForeignKey('exif_data.id'))
                         )
LnkImageClassi = Table('lnk_image_classi', BaseImage.metadata,
                       Column('id_image', Integer, ForeignKey('images.id')),
                       Column('id_classi_data', Integer, ForeignKey('classi_data.id'))
                       )


class Image(BaseImage):
    """
    Table of Images
    """

    __tablename__ = 'images'

    id = Column('id', Integer(), primary_key=True, autoincrement=True,
                doc="""Primary key of image""")

    filename = Column('filename', String(100), nullable=False, doc="""Filename of image""")
    path = Column('path', String(1000), nullable=False, doc="""Filename of image""")
    width = Column('width', String(1000), nullable=False, doc="""size of image""")
    height = Column('height', String(1000), nullable=False, doc="""size of image""")
    datcre = Column('datcre', DateTime, nullable=False, doc="""Date time of insert""")

    exif_datas = relationship('ExifData', secondary=LnkImageExifData, back_populates='images',
                              lazy='subquery')
    classi_datas = relationship('ClassiData', secondary=LnkImageClassi, back_populates='images',
                               lazy='subquery')

    def __init__(self, filename, path, width="", height=""):
        self.filename = filename
        self.path = path
        self.width = width
        self.height = height
        self.datcre = datetime.today()

    def __repr__(self):
        return u'<%s (%s): (%s)>' % (self.__class__.__name__, self.id, self.filename)


class ExifData(BaseImage):
    """ Table of exif data"""
    __tablename__ = 'exif_data'

    id = Column('id', Integer(), primary_key=True, autoincrement=True,
                doc="""Primary key of exif data""")

    name = Column('name', String(1000), nullable=False, doc="""name of data of exif""")
    value = Column('val', String(1000), nullable=False, doc="""value of data of exif""")
    datcre = Column('datcre', DateTime, nullable=False, doc="""Date time of insert""")
    images = relationship(Image, secondary=LnkImageExifData, back_populates='exif_datas',
                          lazy='subquery')

    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.datcre = datetime.today()

    def __repr__(self):
        return u'<%s (%s): (%s)>' % (self.__class__.__name__, self.id, self.name)


class ClassiData(BaseImage):
    """ Table of exif data"""
    __tablename__ = 'classi_data'

    id = Column('id', Integer(), primary_key=True, autoincrement=True,
                doc="""Primary key of exif data""")

    name = Column('name', String(1000), nullable=False, doc="""name of data of exif""")
    datcre = Column('datcre', DateTime, nullable=False, doc="""Date time of insert""")
    images = relationship(Image, secondary=LnkImageClassi, back_populates='classi_datas',
                          lazy='subquery')

    def __init__(self, name):
        self.name = name
        self.datcre = datetime.today()

    def __repr__(self):
        return u'<%s (%s): (%s)>' % (self.__class__.__name__, self.id, self.name)
