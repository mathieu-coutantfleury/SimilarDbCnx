# -*- coding: utf-8 -*-
__author__ = 'Mathieu COUTANT FLEURY'
from similardbcnx.models.model_image import Image, ExifData, LnkImageExifData, ClassiData, LnkImageClassi


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

    def create_classi(self, name, id_img):
        classi = self.fetch_classidata_by_key(name)
        if not classi:
            classi = ClassiData(name)
            self.session.add(classi)
            self.session.flush()

        classi.images.append(self.fetch_images_by_id(id_img))
        self.session.flush()
        return classi.id

    def fetch_images_by_id(self, id_img):
        """ Function to return Image from Db
        :param id_img:
        :return: Image
        :rtype: Image
        """
        return self.session.query(Image).get(id_img)

    def fetch_images_by_filename(self, filename):
        """ Function to return Image from Db
        :param filename:
        :type filename: str
        :return: Image
        :rtype: Image
        """
        lst_img = self.session.query(Image).filter(Image.filename == filename).all()
        if not lst_img:
            return None
        return lst_img[0]

    def fetch_image_by_id_exif(self, id_exif):
        """ Function to get all images associate with exif data
        :param id_exif:
        :return: Image
        """
        return self.session.query(Image).join(LnkImageExifData).join(ExifData).filter(ExifData.id == id_exif)

    def fetch_image_by_id_classi(self, id_classi_data):
        """ Function to get all images associate with classi data
        :param id_classi_data:
        :return: Image
        """
        return self.session.query(Image).join(LnkImageClassi).join(ClassiData).filter(ClassiData.id == id_classi_data)

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

    def fetch_lst_classidata_by_id_filename(self, id_filename):
        """function to return list of classi data
        :param id_filename
        :type id_filename: int
        :return:
        """
        return self.session.query(ClassiData).join(LnkImageClassi).filter(LnkImageClassi.id_image == id_filename)

    def fetch_classidata_by_key(self, key):
        """ function to return classi data
        :param key:
        :return:
        """
        lst_classi = self.session.query(ClassiData).filter(ClassiData.name == key).all()
        if not lst_classi:
            return None
        return lst_classi[0]

    def remove_image(self, id_img):
        img = self.session.query(Image).get(id_img)
        self.session.delete(img)
        self.session.flush()
