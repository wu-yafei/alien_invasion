#coding=gbk
class GameStats():
	
	def __init__(self,ai_settings):
		"""��ʼ��ͳ����Ϣ"""
		self.ai_settings=ai_settings
		self.reset_stats()
		# ��Ϸ������ʱ���ڻ״̬
		self.game_active=False
		# ���κ�����¶���Ӧ������ߵ÷�
		self.high_score=0
		self.get_high_score()
	def reset_stats(self):
		"""��ʼ������Ϸ�����ڼ���ܱ仯��ͳ����Ϣ"""
		self.ships_left=self.ai_settings.ship_limit
		self.score=0
		self.level=1
		
	def get_high_score(self):
		try:
			with open(self.ai_settings.high_score_filename) as f_object:
				self.high_score=int(f_object.read())
		except FileNotFoundError:
			pass
		
			
