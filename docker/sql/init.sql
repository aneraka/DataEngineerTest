create schema auth;

create table auth.user (
    id serial not null,
    username varchar(256) not null,
    password varchar(256) not null,
    created_at timestamptz DEFAULT now() NOT NULL,
    updated_at timestamptz,
    deleted_at timestamptz
);

create schema data;

create table data.hired_employees (
	id int4 NOT NULL,
	"name" varchar(50) NOT NULL,
	datetime varchar(50) NOT NULL,
	department_id int4 NOT NULL,
	job_id int4 NOT NULL,
	create_at timestamptz DEFAULT now() NOT NULL,
    updated_at timestamptz,
    deleted_at timestamptz
);

create table data.departments (
	id int4 NOT NULL,
	department varchar(50) NOT NULL,
	create_at timestamptz DEFAULT now() NOT NULL,
    updated_at timestamptz,
    deleted_at timestamptz
);

create table data.jobs (
	id int4 NOT NULL,
	job varchar(50) NOT NULL,
	create_at timestamptz DEFAULT now() NOT NULL,
    updated_at timestamptz,
    deleted_at timestamptz
);