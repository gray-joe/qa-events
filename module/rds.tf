resource "aws_db_instance" "events_db" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "postgres"
  engine_version       = "13.4"  # Replace with your desired PostgreSQL version
  instance_class       = "db.t2.micro"  # Replace with your desired instance type
  name                 = "my-database"  # Replace with your desired database name
  username             = "db_user"  # Replace with your desired username
  password             = "your_password"  # Replace with your desired password
  parameter_group_name = "default.postgres13"  # Replace with the appropriate parameter group

  tags = {
    Name = "MyDatabase"
  }
}