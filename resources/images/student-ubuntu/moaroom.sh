#! /bin/bash
ROOT_PATH="$(pwd)"
TARGET_ASSIGNMENT="default"

sed_inplace() {
  # BSD sed and GNU sed implements the "-i" option differently.
  case "$OSTYPE" in
    darwin*) sed -i '' "$@" ;;
    bsd*) sed -i '' "$@" ;;
    *) sed -i "$@" ;;
  esac
}

usage() {
  echo "How to use MoaRoom CLI: MoaRoom CLI Tool"
  echo ""
  echo ""
  echo "USAGE"
  echo "  $0 [OPTIONS]"
  echo ""
  echo "OPTIONS"
  echo "  -h, --help"
  echo "    Show this help message and exit"
  echo ""
  echo "  -g, --show-guide"
  echo "    Show the guide of MoaRoom and exit"
  echo ""
  echo "  -l, --list-assignments"
  echo "    List assignments of this lecture"
  echo ""
  echo "  -t, --tree-assignments"
  echo "    List assignments of this lecture with tree-style"
  echo ""
  echo "  -m, --to-assignment"
  echo "    Move to specific assignment directory"
  echo "    Can cd to assignment directory by number of listed assignments"
  echo ""
}

show_guide() {
  echo "MoaRoom Guide: How to use MoaRoom!"
  echo "1. Go to a specific assignment directory by using the cli command"
  echo "    You can use moaroom -h | --help to see how to use it"

}
list_assignments(){
    lines=$((`ls -l assignment/ | wc -l`-1))
    for ((l=1 ; l <= $((lines)) ; l++));
        do
        directory=`ls -l assignment/ | awk 'NR=='"$((l+1))"' {print $9}'`
        echo "$l. $directory"
        done
    echo ""
    echo "Remember the number and get the cmd line with -m | --to-assignment option"
}
tree_assignments(){
    tree "${DIR_PATH_STUDENT}"
}
to_assignment(){
    directory=`ls -l assignment/ | awk 'NR=='"$((TARGET_ASSIGNMENT+1))"' {print $9}'`
    echo "Run this on terminal"
    echo "cd \"${DIR_PATH_STUDENT}/${directory}\""
    
}

while [ $# -gt 0 ]; do
  case $1 in
    -h | --help)              usage; exit 1 ;;
    -g | --show-guide)        show_guide; exit 1 ;;
    -l | --list-assignments)  list_assignments; exit 1 ;;
    -t | --tree-assignments)  tree_assignments; exit 1 ;;
    -m)                       TARGET_ASSIGNMENT=$2; to_assignment; shift ;;
    -m=*)                     TARGET_ASSIGNMENT="${1#*=}"; to_assignment ;;
    --to-assignment)          TARGET_ASSIGNMENT=$2; to_assignment; shift ;;
    --to-assignment=*)        TARGET_ASSIGNMENT="${1#*=}"; to_assignment ;;
    *)
      echo "Unknown option: $1"
      echo "Run '$0 --help' for usage."
      exit 1
  esac
  shift
done
