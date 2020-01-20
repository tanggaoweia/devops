

CREATE TABLE `test`.`apk_info` (
    `build_id` varchar(255) NOT NULL ,
    `type` enum('1','2','3') NOT NULL COMMENT '1dev，2debug，3release',
    `apk_path` varchar(255) CHARACTER SET utf8 COMMENT 'debug剩余私有目录',
    `created_time` datetime(0),
    `update_time` datetime(0),
    PRIMARY KEY (`build_id`, `type`)
);

CREATE TABLE `test`.`commit_and_build_info` (
    `build_id` varchar(255) NOT NULL,
    `commit_id` varchar(255) NOT NULL,
    `created_time` datetime(0),
    PRIMARY KEY (`build_id`),
    FOREIGN KEY (`build_id`) REFERENCES `test`.`apk_info` (`build_id`)
);

CREATE TABLE `test`.`build_and_test_info` (
    `test_run_id` varchar(255)  NOT NULL  ,
    `build_id` varchar(255) NOT NULL,
    `created_time` datetime(0),
    PRIMARY KEY (`test_run_id`),
    FOREIGN KEY (`build_id`) REFERENCES `test`.`apk_info` (`build_id`)
);

CREATE TABLE `test`.`build_description` (
    `build_id` varchar(255) NOT NULL  ,
    `uuid` varchar(255),
    `android_version` varchar(255),
    `app_version` varchar(255),
    `commit_msg` varchar(255),
    `commit_author` varchar(255),
    `branch` varchar(255),
    `build_method` varchar(255),
    `build_author` varchar(255),
    `linked_work_item` varchar(255),
    `created_time` datetime(0),
    PRIMARY KEY (`build_id`),
    FOREIGN KEY (`build_id`) REFERENCES `test`.`apk_info` (`build_id`)

);


CREATE TABLE `test`.`hardware_test_result` (
    `test_run_id` varchar(255) NOT NULL ,
    `airplan_off_to_on` enum('pass','fail', 'null'),
    `airplan_on_to_off` enum('pass','fail', 'null'),
    `mobile4g_off_to_on` enum('pass','fail', 'null'),
    `mobile4g_on_to_off` enum('pass','fail', 'null'),
    `gps_status` enum('true','false'),
    `acc_status` enum('true','false'),
    `sdcard_status` enum('true','false'),
    `wifi_status` enum('true','false'),
    `has_restarted` enum('true','false'),
    `cpu_temp` varchar(255),
    `created_time` datetime(0),
     FOREIGN KEY (`test_run_id`) REFERENCES `test`.`build_and_test_info` (`test_run_id`)
);

CREATE TABLE `test`.`process_test_result` (
    `test_run_id` varchar(255) NOT NULL,
    `mapa_restarted_success` enum('pass','fail'),
    `created_time` datetime(0),
     FOREIGN KEY (`test_run_id`) REFERENCES `test`.`build_and_test_info` (`test_run_id`)
);

CREATE TABLE `test`.`test_result_total`  (
    `test_run_id` varchar(255) NOT NULL,
    `process_total_num` int(9),
    `process_pass_num` int(9),
    `hardware_total_num` int(9),
    `hardware_pass_num` int(9),
    `created_time` datetime(0),
    PRIMARY KEY (`test_run_id`),
    FOREIGN KEY (`test_run_id`) REFERENCES `test`.`build_and_test_info` (`test_run_id`)
);



CREATE TABLE `test`.`request_log`  (
  `request_id` varchar(255) NOT NULL,
  `location_of_error` varchar(255),
  `error_info` varchar(255),
  `created_time` datetime(0),
  `url_info` varchar(255),
  `method` varchar(255),
  `params` varchar(5000),
  `headers` varchar(5000),
  PRIMARY KEY (`request_id`)
);

CREATE TABLE `test`.`operation_log`  (
  `test_run_id` varchar(255) NOT NULL,
  `operation_key` varchar(255),
  `operation_value` varchar(255),
  `is_error` enum('true','false'),
  `created_time` datetime(0),
  FOREIGN KEY (`test_run_id`) REFERENCES `test`.`build_and_test_info` (`test_run_id`)
);

CREATE TABLE `test`.`db_log`  (
  `db_record_id` varchar(255) NOT NULL,
  `db_record_id_type` enum('test_run_id','request_id'),
  `location_of_error` varchar(255),
  `error_info` varchar(255),
  `created_time` datetime(0),
  `sql_info` varchar(5000)
);

CREATE TABLE `test`.`task_info`  (
  `build_id` varchar(255) NOT NULL,
  `test_run_id` varchar(255) NOT NULL,
  `status` enum('0','1') DEFAULT '0',
	`type` enum('1','2','3') NOT NULL COMMENT '1dev，2debug，3release',
  `source` enum('jenkins','web'),
  `created_time` datetime(0),
  `update_time` datetime(0),
  PRIMARY KEY (`build_id`, `test_run_id`),
  FOREIGN KEY (`build_id`) REFERENCES `test`.`apk_info` (`build_id`)
);


CREATE TABLE `test_mapa_machine`.`software_test_result`  (
  `test_run_id` varchar(255) NOT NULL,
  `scene_type` enum('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18') NOT NULL COMMENT '1.day-cloudy-highway, 2day-cloudy-skyway,3day-cloudy-ubran...',
  `precision_rt` varchar(255) NOT NULL,
	`manual_count` int(0) NOT NULL COMMENT '人工标注车框次数',
  `algorithm_count` int(0) NOT NULL COMMENT '算法计算车框次数',
  `overlapping_count` int(0) NOT NULL COMMENT '负荷重叠要求（重叠50%）车框次数',
  `recall_rt` varchar(255) NOT NULL,
  `created_time` datetime(0),
  FOREIGN KEY (`test_run_id`) REFERENCES `test_mapa_machine`.`build_and_test_info` (`test_run_id`)
);

CREATE TABLE `test_mapa_machine`.`software_test_data`  (
  `test_run_id` varchar(255) NOT NULL,
  `algorithmic_data` varchar(255) NOT NULL COMMENT '算法使用数据',
  PRIMARY KEY (`test_run_id`),
  `created_time` datetime(0),
  FOREIGN KEY (`test_run_id`) REFERENCES `test_mapa_machine`.`build_and_test_info` (`test_run_id`)
);
