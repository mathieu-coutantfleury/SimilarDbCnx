# -*- coding: utf-8 -*-
__author__ = 'Mathieu COUTANT FLEURY'
"""File to class to get url from conf"""

import configparser
from pkg_resources import resource_filename


class URLMaker(object):
    """Classs to get url from url"""

    def __init__(self, key, env):
        """
        Get data connection for db
        :param key: Id of session in dictionary _dict_sessions
        :param env: Environnement
        :return:
        """
        self.alias = None

        path_conf_file = resource_filename(__name__, 'conf/%s.conf' % key.lower())
        config = configparser.ConfigParser()
        config.read(path_conf_file)

        type_db = config.get(env, u'%s_TYPE' % key.upper()).strip().lower()
        host = config.get(env, u'%s_HOST' % key.upper()).strip()
        user = config.get(env, u'%s_USER' % key.upper()).strip()
        pasw = config.get(env, u'%s_PASS' % key.upper()).strip()
        port = config.get(env, u'%s_PORT' % key.upper()).strip()

        if type_db == u'mysql':
            # la base est de type "mysql", on recupere les champs specifique (schema et charset)
            schema = config.get(env, u'%s_SCHEMA' % key.upper()).strip()
            charset = config.get(env, u'%s_CHARSET' % key.upper()).strip()

            self.alias = MysqlAlias(user, pasw, host, port, schema, charset=charset)
        else:
            raise Exception(u'TYPE de SGBD unknown %s %s' % (key, env))

    def get_db_url(self, force_db_name=None):
        """
        Retourne l'url de l'alias en paramètre

        :return:
        """
        return self.alias.get_alchemy_url(force_db_name=force_db_name)


class MysqlAlias:
    """
    une classe de paramètre spécifique à mysql
    """

    def __init__(self, user_name, password, host_name, port_number, db_name, charset=None):
        """
        le constructeur d'un alias pour le type Mysql

        :param user_name: le login
        :param password: le mot de passe
        :param host_name: l'adresse ip ou le nom (dns)
        :param port_number: le numéro de port
        :param db_name: le nom de la base de donnée
        """
        self.user_name = user_name
        self.password = password
        self.host_name = host_name
        self.port_number = port_number
        self.db_name = db_name
        self.charset = charset

    def get_alchemy_url(self, force_db_name=None):
        """
        renvoie une url spécifique à sqlAlchemy

        :param: force_db_name (pouvoir surcharger le nom de la base)
        dans le cas de certain projet le nom de la base est calculé
        ou peut varier. Il est donc important de pouvoir modifier
        le nom de la base.

        :param: cpl (non utilisé pour MYSQL)
        """

        db = force_db_name if force_db_name else self.db_name

        url = u'mysql://%s%s@%s:%s/%s' % (self.user_name,
                                          ':%s' % self.password if self.password else '',
                                          self.host_name, self.port_number, db)

        # on laisse la possibilité d'ajouter des paramètres du type ?charset=utf8
        if self.charset:
            url += '?charset=%s' % self.charset

        return url
