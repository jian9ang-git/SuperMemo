from lesson.lesson import LessonCart


def is_active_lesson(request, user):

    lesson_cart = LessonCart(request)
    if lesson_cart.len() == 0:
        if user.profile.lessons.filter(active_lesson=True).exists():
            active_lesson = user.profile.lessons.get(active_lesson=True)
            active_lesson_id = active_lesson.id
            if active_lesson_id not in lesson_cart:
                lesson_cart[str(active_lesson_id)] = {'lesson': active_lesson}
                return active_lesson_id
    else:
        active_lesson = user.profile.lessons.get(active_lesson=True)
        active_lesson_id = active_lesson.id
        if active_lesson_id not in lesson_cart:
            return