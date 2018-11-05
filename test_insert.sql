insert into ilifu_user (username, email, public_key, first_name, last_name, contact_number, institution)
	values ('sam','sam@test.test', 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCzsKiJWkZZN4U7ZlHJPZGEoWBQwSE1k5jvEsWTf7rL+4p4RUdiG4HgfcgoNMtFf3+sp9VtcKA1BoemmKPOImU9kWbI39fH9Sivqh9wfc4VDnjqka47YWb/mtbwbeuQQhYfEEMMk0B9f/giOtvqmVUdwu1YFhIJ+2nfCjx4a4KY2W7EezgAFXnv9cjxACX4QRsZveaA/EBR7ccsxT8SRbCHtQx+VDrNb1Vgmbi8JIJOHfi9ir8H67p2mvePf1nxMrGOCoN2g2440XKFKQqVmZjQ1mm2UrB6ivDl4uKpfpHeDLnfIttD/1KCgucKwIXDsZuQaLjBpWpBBj9Wf9zTWQqJ jasper@Jaspers-MBP',
		'Sam','Test','1234567', 'UCT');

insert into project (name, resource_tree_posn, parent_resource_fraction)
	values ('root', '{1, NULL, NULL, NULL, NULL}', 1.0);

insert into project (name, resource_tree_posn, parent_resource_fraction)
	values ('IDIA', '{1, 1, NULL, NULL, NULL}', 0.3);

insert into project (name, resource_tree_posn, parent_resource_fraction)
	values ('CBIO', '{1, 2, NULL, NULL, NULL}', 0.4);

insert into project (name, resource_tree_posn, parent_resource_fraction)
	values ('DIRISA', '{1, 3, NULL, NULL, NULL}', 0.3);

