#!/bin/sh

exec kvm -m 128 -smp 1 -drive file=tmpNsRv_Q.qcow2 "$@"
