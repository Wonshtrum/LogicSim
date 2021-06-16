for file in `find $1 -type f -name '*.py'`
do
	if grep -nE --color=always $2 $file; then
		echo $file
		echo
	fi
done
