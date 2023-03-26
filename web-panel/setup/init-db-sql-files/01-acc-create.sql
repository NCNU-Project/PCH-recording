CREATE TABLE `acc` (
	    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
	    `method` VARCHAR(16) DEFAULT '' NOT NULL,
	    `from_tag` VARCHAR(128) DEFAULT '' NOT NULL,
	    `to_tag` VARCHAR(128) DEFAULT '' NOT NULL,
	    `callid` VARCHAR(255) DEFAULT '' NOT NULL,
	    `sip_code` VARCHAR(3) DEFAULT '' NOT NULL,
	    `sip_reason` VARCHAR(128) DEFAULT '' NOT NULL,
	    `time` DATETIME NOT NULL
);

CREATE INDEX callid_idx ON acc (`callid`);

INSERT INTO version (table_name, table_version) values ('acc','5');

CREATE TABLE `acc_cdrs` (
	    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
	    `start_time` DATETIME DEFAULT '2000-01-01 00:00:00' NOT NULL,
	    `end_time` DATETIME DEFAULT '2000-01-01 00:00:00' NOT NULL,
	    `ring_time` DATETIME NOT NULL DEFAULT '2000-01-01 00:00:00',
	    `duration` FLOAT(10,3) DEFAULT 0 NOT NULL,
	    `callid` VARCHAR(255) DEFAULT '' NOT NULL
);

CREATE INDEX start_time_idx ON acc_cdrs (`start_time`);

INSERT INTO version (table_name, table_version) values ('acc_cdrs','2');

CREATE TABLE `missed_calls` (
	    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
	    `method` VARCHAR(16) DEFAULT '' NOT NULL,
	    `from_tag` VARCHAR(128) DEFAULT '' NOT NULL,
	    `to_tag` VARCHAR(128) DEFAULT '' NOT NULL,
	    `callid` VARCHAR(255) DEFAULT '' NOT NULL,
	    `sip_code` VARCHAR(3) DEFAULT '' NOT NULL,
	    `sip_reason` VARCHAR(128) DEFAULT '' NOT NULL,
	    `time` DATETIME NOT NULL
);

CREATE INDEX callid_idx ON missed_calls (`callid`);

INSERT INTO version (table_name, table_version) values ('missed_calls','4');

ALTER TABLE acc ADD COLUMN src_user VARCHAR(64) NOT NULL DEFAULT '';
ALTER TABLE acc ADD COLUMN src_domain VARCHAR(128) NOT NULL DEFAULT '';
ALTER TABLE acc ADD COLUMN src_ip varchar(64) NOT NULL default '';
ALTER TABLE acc ADD COLUMN dst_ouser VARCHAR(64) NOT NULL DEFAULT '';
ALTER TABLE acc ADD COLUMN dst_user VARCHAR(64) NOT NULL DEFAULT '';
ALTER TABLE acc ADD COLUMN dst_domain VARCHAR(128) NOT NULL DEFAULT '';
ALTER TABLE missed_calls ADD COLUMN src_user VARCHAR(64) NOT NULL DEFAULT '';
ALTER TABLE missed_calls ADD COLUMN src_domain VARCHAR(128) NOT NULL DEFAULT '';
ALTER TABLE missed_calls ADD COLUMN src_ip varchar(64) NOT NULL default '';
ALTER TABLE missed_calls ADD COLUMN dst_ouser VARCHAR(64) NOT NULL DEFAULT '';
ALTER TABLE missed_calls ADD COLUMN dst_user VARCHAR(64) NOT NULL DEFAULT '';
ALTER TABLE missed_calls ADD COLUMN dst_domain VARCHAR(128) NOT NULL DEFAULT '';

