resource "aws_route53_record" "db" {
  zone_id = var.hosted_zone_id
  name = "${var.identifier}.${var.domain_suffix}"
  type = "CNAME"
  ttl = "300"
  records = ["${aws_db_instance.db.address}"]
}
