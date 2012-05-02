web: python mycelium/manage.py grab_manifest --settings=envs.live;python mycelium/manage.py collectstatic --settings=envs.livepython mycelium/manage.py run_gunicorn -b "0.0.0.0:$PORT" --workers=4 --settings=envs.live
celery: python mycelium/manage.py celeryd -c 2 -B --settings=envs.live
