import zlib

class CHASH(object) :
	nodes	= []
	ppos	= []
	pos		= dict()
	ok		= False 
	ptr		= -1

	def __init__(self, config, replics=179) :
		self.nodes = config
		self.ok = True
		if replics < 1 :
			self.ok = False
		if len(config) < 1 :
			self.ok = False

		for i in range(len(config)) :
			for j in range(replics) :
				hash = self._hash(config[i]+":"+str(j))
				self.pos[hash] = i;
		for key in sorted(self.pos.keys()) :
			self.ppos.append(key)
	
	def get_node(self, key) :
		if not self.ok :
			return False

		hash = self._hash(key)
		pos = self._find_pos(hash)
		self.ptr = pos

		return self.nodes[self.pos[pos]]

	def next_node(self) :
		if not self.ok :
			return False
		if self.ptr == -1 :
			return False

		old = self.pos[self.ptr]
		npos = self._find_pos(self.ptr+1)
		new = self.pos[npos]
		while new == old :
			npos = self._find_pos(npos+1)
			new = self.pos[npos]

		self.ptr = npos
		return self.nodes[new]

	def _find_pos(self, hash) :
		for pos in self.ppos :
			if pos >= hash :
				return pos
		return self.ppos[0]

	def _hash(self, key) :
		return abs(zlib.crc32(key))

'''
import sys
import hashlib

cs = CHASH(['0', '1', '2', '3', '4', '5', '6']);
for i in range(1000) :
	m = hashlib.md5()
	m.update('abcd'+str(i))
	key = m.hexdigest()
	print cs.get_node(key)
	print cs.next_node()
	print cs.next_node()
	print cs.next_node()
	print cs.next_node()
'''
