run-db:
	docker run --name tribe_postgres -p 15432:15432 -e POSTGRES_PASSWORD=mysuperpassword -e POSTGRES_DB=tribe -v ${PWD}/db_data:/var/lib/postgresql/data -d postgres