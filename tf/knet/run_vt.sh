#! /usr/bin/env bash

MYDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${MYDIR}

find log/* -mtime +60 -exec rm -rf {} \;
ts=`date +%Y%m%d%H%M%S`

vt_log=log/vt.log.${ts}

# train with only video history
# (./fetchdata_vt.sh && ./preprocess_vt.sh) > ${vt_log} 2>&1

# train with video and article history
(./fetchdata_vt_all.sh && ./preprocess_vt.sh) > ${vt_log} 2>&1
