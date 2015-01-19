import logging

log_format = '%(asctime)s  [P%(process)s] %(levelname)-8s : %(module)s - %(message)s'
formatter = logging.Formatter(log_format)

out_logger = logging.getLogger('out_logger')
out_logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
out_logger.addHandler(stream_handler)

main_logger = logging.getLogger('main_logger')
main_logger.setLevel(logging.DEBUG)
main_file_handler = logging.FileHandler('logs/main.log')
main_file_handler.setLevel(logging.DEBUG)
main_file_handler.setFormatter(formatter)
main_logger.addHandler(main_file_handler)

task_logger = logging.getLogger('task_logger')
task_logger.setLevel(logging.DEBUG)
task_file_handler = logging.FileHandler('logs/task.log')
task_file_handler.setLevel(logging.DEBUG)
task_file_handler.setFormatter(formatter)
main_logger.addHandler(task_file_handler)


