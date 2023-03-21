# crate kamailio RW/RO user
mysql -uroot -p"${DBROOTPW}" <<EOF
CREATE USER '${DBRWUSER}'@'%' IDENTIFIED WITH mysql_native_password BY '${DBRWPW}';
CREATE USER '${DBROUSER}'@'%' IDENTIFIED WITH mysql_native_password BY '${DBROPW}';
GRANT ALL ON ${DBNAME}.* TO '${DBRWUSER}'@'%';
GRANT SELECT ON ${DBNAME}.* TO '${DBROUSER}'@'%';
FLUSH PRIVILEGES;
EOF
