# -*- coding: utf-8 -*-
__author__ = 'Mathieu COUTANT FLEURY'
"""File to define Session Db"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from similardbcnx.db.db_url_maker import URLMaker

log = logging.getLogger('main')


class SessionManager(object):
    """
    Classe to manage session to DB
    """

    # Define only one instance
    _instance = None

    # Default params to create engine
    echo = False
    pool_size = 5
    pool_recycle = -1

    # Default params to open session
    autoflush = True
    autocommit = True
    expire_on_commit = True

    # Define environnement
    DEV = 'DEV'
    PROD = 'PROD'
    LST_ENVS = [DEV, PROD]
    _ENV = DEV

    # Dict to keep all session open by env
    _dict_sessions = dict()

    def __new__(cls, *args, **kwargs):
        """
        Singleton Class
        """
        if not cls._instance:
            cls._instance = super(SessionManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def set_environement(self, env):
        """ Function to define connection environnement
        :param env:
        :type env: str
        :return:
        """
        if env.upper() in self.LST_ENVS:
            self._ENV = env.upper()
            log.info('ENV=%s' % self._ENV)

    def kill_session(self, key, env=None):
        """ Function to close en del session in dictionary
        :param key: Id of session in dictionary _dict_sessions
        :param env:
        :return: True if one of session is close
        """
        if env:
            if key in self._dict_sessions[env]:
                self._dict_sessions[env][key].close()
                self._dict_sessions[env][key].bind.dispose()
                del self._dict_sessions[env][key]
                return True
        return False

    def kill_all_sessions(self):
        """Function to stop all session in dictionary
        :return: True if one of session if close
        """
        res = False

        for env in self.LST_ENVS:
            if env in self._dict_sessions:
                clone = self._dict_sessions[env].copy()

                for key in clone.keys():
                    statut = self.kill_session(key, env=env)
                    if not res and statut:
                        res = True
        return res

    def get_or_create_session(self, key, env, extraParams={}):
        """
        Retourne la session sqlalchemy

        :param key: Id of session in dictionary _dict_sessions
        :param env: environement of session
        :return: SqlAlchemySession object
        """

        # Add environnement in dictionary.
        if env not in self._dict_sessions:
            self._dict_sessions[env] = {}

        if key not in self._dict_sessions[env]:
            um = URLMaker(key, env)
            url = um.get_db_url()

            engine = create_engine(url, echo=self.echo, pool_size=self.pool_size, pool_recycle=self.pool_recycle,
                                   **extraParams)
            session = sessionmaker(bind=engine, autoflush=self.autoflush, autocommit=self.autocommit,
                                   expire_on_commit=self.expire_on_commit)

            self._dict_sessions[env][key] = session
            # log.info('bind : %s' % session.bind)

        return self._dict_sessions[env][key]()
