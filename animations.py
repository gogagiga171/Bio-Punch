import os
from classes.AnimationFrame import AnimationFrame
from classes.Animation import Animation
from classes.Vector import Vector

def generate_frame_set_from_dir(path, offset, size, codes, player):
    m = []
    for i, name in enumerate(os.listdir(path)):
        m.append(AnimationFrame(path+"/"+name, offset, size, codes[i], player))
    return m

def generate_animations(player):
    default_offset = Vector([-45, -40])
    size = 1/2

    # Idle right
    idle_right_animation_frames = generate_frame_set_from_dir("resources/player/idle_r", default_offset, size, [None, None, None, None, None, None, None, None, None, None, None, None, None], player)
    idle_right_animation = Animation(idle_right_animation_frames, True, 12)

    # Idle left
    idle_left_animation_frames = generate_frame_set_from_dir("resources/player/idle_l", default_offset, size, [None, None, None, None, None, None, None, None, None, None, None, None, None], player)
    idle_left_animation = Animation(idle_left_animation_frames, True, 12)

    # Punch right
    punch_right_animation_frames = generate_frame_set_from_dir("resources/player/punch_r", default_offset, size, [None, None, player.punch.hit, None, player.reset_animation], player)
    punch_right_animation = Animation(punch_right_animation_frames, False, 12)

    # Punch left
    punch_left_animation_frames = generate_frame_set_from_dir("resources/player/punch_l", default_offset, size, [None, None, player.punch.hit, None, player.reset_animation], player)
    punch_left_animation = Animation(punch_left_animation_frames, False, 12)

    # Kick right
    kick_right_animation_frames = generate_frame_set_from_dir("resources/player/kick_r", default_offset, size, [None, None, None, None, None, None, None, None, None, player.kick.hit, None, None, None, None, None, player.reset_animation], player)
    kick_right_animation = Animation(kick_right_animation_frames, False, 24)

    # Kick left
    kick_left_animation_frames = generate_frame_set_from_dir("resources/player/kick_l", default_offset, size, [None, None, None, None, None, None, None, None, None, player.kick.hit, None, None, None, None, None, player.reset_animation], player)
    kick_left_animation = Animation(kick_left_animation_frames, False, 24)

    # Run right
    run_right_animation_frames = generate_frame_set_from_dir("resources/player/run_r", default_offset, size, [None, None, None, None, None, None, None, None, None, None, None, None, None], player)
    run_right_animation = Animation(run_right_animation_frames, True, 24)

    # Run left
    run_left_animation_frames = generate_frame_set_from_dir("resources/player/run_l", default_offset, size, [None, None, None, None, None, None, None, None, None, None, None, None, None], player)
    run_left_animation = Animation(run_left_animation_frames, True, 24)

    # Crouch right
    crouch_right_animation_frames = generate_frame_set_from_dir("resources/player/crouch_r", default_offset, size, [None, None, None, None, None, None, None, None, None, None, None, None, None], player)
    crouch_right_animation = Animation(crouch_right_animation_frames, True, 12)

    # Crouch left
    crouch_left_animation_frames = generate_frame_set_from_dir("resources/player/crouch_l", default_offset, size, [None, None, None, None, None, None, None, None, None, None, None, None, None], player)
    crouch_left_animation = Animation(crouch_left_animation_frames, True, 12)

    # Crouch punch right
    crouch_punch_right_animation_frames = generate_frame_set_from_dir("resources/player/crouch_punch_r", default_offset, size, [None, None, player.crouch_punch.hit, None, None, player.reset_animation], player)
    crouch_punch_right_animation = Animation(crouch_punch_right_animation_frames, False, 12)

    # Crouch punch left
    crouch_punch_left_animation_frames = generate_frame_set_from_dir("resources/player/crouch_punch_l", default_offset, size, [None, None, player.crouch_punch.hit, None, None, player.reset_animation], player)
    crouch_punch_left_animation = Animation(crouch_punch_left_animation_frames, False, 12)

    # Crouch kick right
    crouch_kick_right_animation_frames = generate_frame_set_from_dir("resources/player/crouch_kick_r", default_offset, size, [None, None, None, player.crouch_kick.hit, None, None, player.reset_animation], player)
    crouch_kick_right_animation = Animation(crouch_kick_right_animation_frames, False, 12)

    # Crouch kick left
    crouch_kick_left_animation_frames = generate_frame_set_from_dir("resources/player/crouch_kick_l", default_offset, size, [None, None, None, player.crouch_kick.hit, None, None, player.reset_animation], player)
    crouch_kick_left_animation = Animation(crouch_kick_left_animation_frames, False, 12)

    # Crawl right
    crawl_right_animation_frames = generate_frame_set_from_dir("resources/player/crawl_r", default_offset, size, [None, None, None, None, None, None, None, None, None, None, None, None, None], player)
    crawl_right_animation = Animation(crawl_right_animation_frames, True, 10)

    # Crawl left
    crawl_left_animation_frames = generate_frame_set_from_dir("resources/player/crawl_l", default_offset, size, [None, None, None, None, None, None, None, None, None, None, None, None, None], player)
    crawl_left_animation = Animation(crawl_left_animation_frames, True, 10)

    # Jump right
    jump_right_animation_frames = generate_frame_set_from_dir("resources/player/jump_r", default_offset, size, [None], player)
    jump_right_animation = Animation(jump_right_animation_frames, True, 12)

    # Jump left
    jump_left_animation_frames = generate_frame_set_from_dir("resources/player/jump_l", default_offset, size, [None], player)
    jump_left_animation = Animation(jump_left_animation_frames, True, 12)

    # Jump punch right
    jump_punch_right_animation_frames = generate_frame_set_from_dir("resources/player/jump_punch_r", default_offset, size, [None, None, player.flight_punch.hit, None, player.reset_animation], player)
    jump_punch_right_animation = Animation(jump_punch_right_animation_frames, False, 24)

    # Jump punch left
    jump_punch_left_animation_frames = generate_frame_set_from_dir("resources/player/jump_punch_l", default_offset, size, [None, None, player.flight_punch.hit, None, player.reset_animation], player)
    jump_punch_left_animation = Animation(jump_punch_left_animation_frames, False, 24)

    # Jump kick right
    jump_kick_right_animation_frames = generate_frame_set_from_dir("resources/player/jump_kick_r", default_offset, size, [None, None, None, None, None, None, None, player.flight_kick.hit, None, None, player.reset_animation], player)
    jump_kick_right_animation = Animation(jump_kick_right_animation_frames, False, 24)

    # Jump kick left
    jump_kick_left_animation_frames = generate_frame_set_from_dir("resources/player/jump_kick_l", default_offset, size, [None, None, None, None, None, None, None, player.flight_kick.hit, None, None, player.reset_animation], player)
    jump_kick_left_animation = Animation(jump_kick_left_animation_frames, False, 24)

    animations_set = {
        "idle_right": idle_right_animation,
        "idle_left": idle_left_animation,
        "punch_right": punch_right_animation,
        "punch_left": punch_left_animation,
        "kick_right": kick_right_animation,
        "kick_left": kick_left_animation,
        "run_right": run_right_animation,
        "run_left": run_left_animation,
        "crouch_right": crouch_right_animation,
        "crouch_left": crouch_left_animation,
        "crouch_punch_right": crouch_punch_right_animation,
        "crouch_punch_left": crouch_punch_left_animation,
        "crouch_kick_right": crouch_kick_right_animation,
        "crouch_kick_left": crouch_kick_left_animation,
        "crawl_right": crawl_right_animation,
        "crawl_left": crawl_left_animation,
        "jump_right": jump_right_animation,
        "jump_left": jump_left_animation,
        "jump_punch_right": jump_punch_right_animation,
        "jump_punch_left": jump_punch_left_animation,
        "jump_kick_right": jump_kick_right_animation,
        "jump_kick_left": jump_kick_left_animation
    }

    return animations_set