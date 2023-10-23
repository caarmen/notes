error=0
for project in notes
do
  ruff check $project || error=$?
  black $project || error=$?
  isort --profile black $project || error=$?
done
pytest --junitxml="reports/junit.xml" notes/tests || error=$?
exit $error
