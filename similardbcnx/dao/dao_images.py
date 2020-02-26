# -*- coding: utf-8 -*-
__author__ = 'Mathieu COUTANT FLEURY'
from similardbcnx.models.model_image import Image, ExifData, LnkImageExifData


class DaoImages(object):
    """
    Une classe groups function to access db Images
    """

    def __init__(self, i_dbpe):
        self.session = i_dbpe

    def create_image(self, path_folder, filename, width, height):
        image_new = Image(filename, path_folder, width=width, height=height)
        self.session.add(image_new)
        self.session.flush()
        return image_new.id

    def create_exif(self, name, value, id_img):
        exif = self.fetch_exifdata_by_key_value(name, value)
        if not exif:
            exif = ExifData(name, value)
            self.session.add(exif)
            self.session.flush()

        exif.images.append(self.fetch_images_by_id(id_img))
        self.session.flush()
        return exif.id

    def fetch_images_by_id(self, id_img):
        """ Function to return Image from Db
        :param id_img:
        :return:
        """
        return self.session.query(Image).get(id_img)

    def fetch_images_by_filename(self, filename):
        """ Function to return Image from Db
        :param filename:
        :type filename: str
        :return:
        """
        return self.session.query(Image).filter(Image.filename == filename)

    def fetch_lst_exifdata_by_id_filename(self, id_filename):
        """function to return list of exif data
        :param id_filename
        :type id_filename: int
        :return:
        """
        return self.session.query(ExifData).join(LnkImageExifData).filter(LnkImageExifData.id_image == id_filename)

    def fetch_exifdata_by_key_value(self, key, value):
        """ function to return exif data
        :param key:
        :param value:
        :return:
        """
        lst_exif = self.session.query(ExifData).filter(ExifData.name == key, ExifData.value == value).all()
        if not lst_exif:
            return None
        return lst_exif[0]

    def remove_image(self, id_img):
        img = self.session.query(Image).get(id_img)
        self.session.delete(img)
        self.session.flush()
