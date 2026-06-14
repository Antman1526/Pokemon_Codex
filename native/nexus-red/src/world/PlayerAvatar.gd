extends ColorRect

var move_speed := 220.0
var bounds := Rect2(Vector2(40, 70), Vector2(1200, 560))


func _ready() -> void:
	color = Color("e94b4b")
	custom_minimum_size = Vector2(32, 32)
	size = Vector2(32, 32)


func _process(delta: float) -> void:
	var direction := Vector2.ZERO
	if Input.is_action_pressed("ui_right"):
		direction.x += 1.0
	if Input.is_action_pressed("ui_left"):
		direction.x -= 1.0
	if Input.is_action_pressed("ui_down"):
		direction.y += 1.0
	if Input.is_action_pressed("ui_up"):
		direction.y -= 1.0
	if direction != Vector2.ZERO:
		direction = direction.normalized()
	position += direction * move_speed * delta
	position.x = clamp(position.x, bounds.position.x, bounds.position.x + bounds.size.x)
	position.y = clamp(position.y, bounds.position.y, bounds.position.y + bounds.size.y)
