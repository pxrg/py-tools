#!usr/bin/env python
#-*-coding:utf-8-*-

import logging
import logging.handlers as handlers
import os 

PATH = os.path.abspath('.')


class CustomLogger(object):
    # Configuracao geral do log, formato de data e formato da msg
    config = None
    config_file = None
    config_mail = None
    init = False
    _logger = None
    _use_mail = False

    @classmethod
    def _init(self):  
        if not self.init:
            self.config = {
                    'datefmt' : '%d/%m/%Y-%H:%M:%S',
                    'format' : '\n%(asctime)s - %(name)s - [%(levelname)s] : %(message)s'
                }

            self.config_file = {
            	'filename' : os.path.join(PATH, 'log/app_out.log'),
            	'maxBytes':1024*1024,
            	'backupCount': 10
            }

            self.config_mail = {
                'mailhost':('smtp.email.com.br',25), # (host, port) or host
                'fromaddr': 'conta@dominio.com.br',
                'toaddrs': ['conta@dominio.com.br'], # lista dos enderecos a serem enviados 
                'subject': 'Alerta / Erro no Sistema' ,
                'credentials' : None,# (user, passw)
                'secure' : None,
            }
            # Passando as configuracoes para o log
            logging.basicConfig(**config)
            if not os.path.exists(os.path.join(PATH, 'log')):
                os.mkdir(os.path.join(os.path.join(PATH, 'log')))

            # Criando uma instancia de Logger com o nome do modulo especifico
            self._logger = logging.getLogger(__name__)
            # Setando o level do log
            self._logger.setLevel(logging.INFO)
            # Criando o handler na qual sera a saida do log com as configuracoes

            ## Handler para saida em arquivo, provendo rotatividade de acordo com o 
            ## tamanho de limite em bytes definido
            handler_file = handlers.RotatingFileHandler(**self.config_file)

            ## Handler para envio da saida do log por email
            ## todas as configuracoes sao definidas em config_mail
            handler_mail = handlers.SMTPHandler(**self.config_mail)
            handler_mail.setLevel(logging.ERROR)

            # Criando uma instancia para formatar a saida do log
            formatter = logging.Formatter(self.config.get('format')) # formato do texto em geral
            formatter.datefmt = self.config.get('datefmt') # formato da data

            # Adicionando as configuracoes do handler e formatter
            handler_file.setFormatter(formatter)
            handler_mail.setFormatter(formatter)

            self._logger.addHandler(handler_file)
            if self._use_mail:
                self._logger.addHandler(handler_mail)
            self.init = True

    @classmethod
    def log_info(self, msg):
        self._init()
        self._logger.info(msg)

    @classmethod
    def log_exception(self, ex):
        self._init()
        self._logger.exception(ex)        
