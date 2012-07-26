<?php
class CHASH {
	private		$nodes;		//aaray
	private		$pos;		//array
	private		$ok;		//bool

	private		$ptr;

	function __construct($config, $reps=7)
	{
		$this->ptr = -1;
		$this->pos = array();

		$this->nodes = $config;
		$this->ok = true;
		if ($reps < 1) $this->ok = false;
		if (empty($config) || !is_array($config) || count($config) < 1)
			$this->ok = false;

		foreach ($config as $k => $v) {
			for ($i=0; $i<$reps; $i++) {
				$hash = $this->_hash($v.":".$i);
				$this->pos[$hash] = $k;
			}
		}
		ksort($this->pos, SORT_NUMERIC);
	}

	function __destruct()
	{
		unset($this->nodes);
		unset($this->pos);
		unset($this->ok);
	}

	function get_node($key)
	{
		if (!$this->ok) return false;

		$hash = $this->_hash($key);
		$this->ptr = $pos = $this->_find_pos($hash);

		return $this->nodes[$this->pos[$pos]];
	}

	function next_node()
	{
		if (!$this->ok) return false;
		if ($this->ptr == -1) return false;

		$hash = $this->ptr + 1;
		$this->ptr = $pos = $this->_find_pos($hash);

		return $this->nodes[$this->pos[$pos]];

	}

	function _find_pos($hash)
	{
		foreach ($this->pos as $k => $v) {
			if ($k >= $hash) return $k;
		}

		foreach ($this->pos as $k => $v) {
			return $k;
		}

		//never to here
		return 0;
	}

	function _hash($str)
	{
		return abs(crc32($str));
	}
}
?>
