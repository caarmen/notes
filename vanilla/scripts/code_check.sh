error=0
for project in app tests
do
  pylint $project || error=$?
done
python -m unittest || error=$?
exit $error
