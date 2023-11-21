project_path=$(dirname $0)/../notes

pushd $project_path
python -m manage migrate
python -m manage runserver 8003
