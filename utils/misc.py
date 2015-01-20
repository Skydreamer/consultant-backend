import logging

main_logger = logging.getLogger('main_logger')
task_logger = logging.getLogger('task_logger')

def config_loggers():
    log_format = '%(asctime)s  [P%(process)s] %(levelname)-8s : %(module)s - %(message)s'
    formatter = logging.Formatter(log_format)

    main_logger.setLevel(logging.ERROR)
    file_handler = logging.FileHandler('logs/main.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    main_logger.addHandler(file_handler)
    main_logger.addHandler(stream_handler)

    task_logger.setLevel(logging.ERROR)
    task_file_handler = logging.FileHandler('logs/task.log')
    task_file_handler.setLevel(logging.DEBUG)
    task_file_handler.setFormatter(formatter)
    main_logger.addHandler(task_file_handler)
