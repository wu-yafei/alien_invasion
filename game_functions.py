#coding=gbk
import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
	# �����ӵ�λ��
	bullets.update()
	# ɾ������ʧ���ӵ�
	for bullet in bullets.copy():
		if bullet.rect.bottom<=0:
			bullets.remove(bullet)
	
	check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,
			aliens,bullets)
	

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,
		aliens,bullets):
	"""��Ӧ�ӵ��������˵���ײ"""
	# ɾ��������ײ��������
	collisions=pygame.sprite.groupcollide(bullets,aliens,False,True)
	
	if collisions:
		for aliens in collisions.values():
			stats.score+=ai_settings.alien_points*len(aliens)
			sb.prep_score()
		check_high_score(stats,sb)
	
	if len(aliens)==0:
		# ɾ�������ӵ����½�һȺ������
		bullets.empty()
		ai_settings.increase_speed()
		
		# ��ߵȼ�
		stats.level+=1
		sb.prep_level()
		
		create_fleet(ai_settings,screen,ship,aliens)
		
def fire_bullet(ai_settings,screen,ship,bullets):
	# �������ӵ���������뵽����bullets��
	if len(bullets)<ai_settings.bullets_allowed:
		new_bullet=Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)

def get_number_rows(ai_settings,ship_height,alien_height):
	"""������Ļ�����ɶ�����������"""
	available_space_y=(ai_settings.screen_height-
						(3*alien_height)-ship_height)
	number_rows=int(available_space_y/(2*alien_height))
	return number_rows
	
def get_number_aliens_x(ai_settings,alien_width):
	# ����һ�п����ɶ��ٸ�������
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x
	
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	#����һ�������˲����뵽��ǰ��
	alien=Alien(ai_settings,screen)
	alien_width=alien.rect.width
	alien.x=alien_width+2*alien_width*alien_number
	alien.rect.x=alien.x
	alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
	aliens.add(alien)
		
def create_fleet(ai_settings,screen,ship,aliens):
	"""����������Ⱥ"""
	# ����һ�������ˣ�������һ�п����ɶ��ٸ�������
	alien=Alien(ai_settings,screen)	
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows=get_number_rows(ai_settings,ship.rect.height,
				alien.rect.height)
	
	#������һ��������
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings,screen,aliens,alien_number,
					row_number)
					
def save_high_score(ai_settings,stats):
	"""����߷�д���ļ�����"""
	with open(ai_settings.high_score_filename,'w') as f_obj:
		f_obj.write(str(stats.high_score))

def check_keydown_events(event,ai_settings,screen,stats,ship,bullets):
	"""��Ӧ����"""
	if event.key==pygame.K_RIGHT:
		ship.moving_right=True
	elif event.key==pygame.K_LEFT:
		ship.moving_left=True
	elif event.key==pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	elif event.key==pygame.K_q:
		save_high_score(ai_settings,stats)
		sys.exit()

def check_keyup_events(event,ship):
	"""��Ӧ�ɿ�"""
	if event.key==pygame.K_RIGHT:
		ship.moving_right=False
	elif event.key==pygame.K_LEFT:
		ship.moving_left=False

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
	"""��Ӧ����������¼�"""
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			save_high_score(ai_settings,stats)
			sys.exit()
		elif event.type==pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,stats,ship,bullets)	
		elif event.type==pygame.KEYUP:
			check_keyup_events(event,ship)
		elif event.type==pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y=pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,stats,sb,play_button,ship,
					aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens
		,bullets,mouse_x,mouse_y):
	"""����ҵ���Play��ťʱ��ʼ��Ϸ"""
	button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_clicked and not stats.game_active:
		# ������Ϸ����
		ai_settings.initialize_dynamic_settings()
		# ���ع��
		pygame.mouse.set_visible(False)
		# ������Ϸͳ����Ϣ
		stats.reset_stats()
		stats.game_active=True
		
		# ���üǷ���ͼ��
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		
		# ����������б����ӵ��б�
		aliens.empty()
		bullets.empty()
		
		# ����һȺ�µ������ˣ����÷ɴ�����
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
				
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
	"""������Ļͼ�񣬲��л�������Ļ"""
	# ÿ��ѭ�����ػ���Ļ
	screen.fill(ai_settings.bg_color)
	
	# �ڷɴ��������˺����ػ������ӵ�
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	
	ship.blitme()
	aliens.draw(screen)
	# ��ʾ�÷�
	sb.show_score()
	
	#�����Ϸ���ڷǻ״̬���ͻ���Play��ť
	if not stats.game_active:
		play_button.draw_button()
	
	# ��������Ƶ���Ļ�ɼ�
	pygame.display.flip()
	
def check_fleet_edges(ai_settings,aliens):
	"""�������˵����Եʱ��ȡ��Ӧ�Ĵ�ʩ"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break
	
def change_fleet_direction(ai_settings,aliens):
	"""�ı��������ƶ�����"""
	for alien in aliens.sprites():
		alien.rect.y+=ai_settings.fleet_drop_speed
	ai_settings.fleet_direction*=-1
	
def update_aliens(ai_settings,stats,screen,sb,ship,aliens,bullets):
	"""����Ƿ���������λ����Ļ��Ե��������������Ⱥ�����������˵�λ��"""
	check_fleet_edges(ai_settings,aliens)
	aliens.update()
	
	# ��������˺ͷɴ�֮�����ײ
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)
	# ����Ƿ��������˵�����Ļ�ײ�
	check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets)
		
def ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets):
	"""��Ӧ������ײ���ɴ�"""
	if stats.ships_left>0:
		# ��ships_left��1
		stats.ships_left-=1
		
		# ���¼Ƿ���
		sb.prep_ships()

		# ��������˺��ӵ�
		aliens.empty()
		bullets.empty()

		# ����һȺ�������ˣ������ɴ��ŵ���Ļ�ײ�����
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()

		# ��ͣ
		sleep(0.5)
	else:
		stats.game_active=False
		pygame.mouse.set_visible(True)
	
def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets):
	# ����Ƿ��������˵�����Ļ�ײ�
	screen_rect=screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom>=screen_rect.bottom:
			ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
			break
			
def check_high_score(stats,sb):
	"""����Ƿ������µ���ߵ÷�"""
	if stats.score>stats.high_score:
		stats.high_score=stats.score
		sb.prep_high_score()
