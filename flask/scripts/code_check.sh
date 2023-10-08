error=0
for project in app alembic tests
do
  ruff check $project || error=$?
  black $project || error=$?
  isort --profile black $project || error=$?
done
pytest || error=$?
exit $error
