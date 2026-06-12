CREATE UNIQUE INDEX Index_Map_Episode_Warrens ON Map(EpisodeId)
  WHERE HellKeepWarrensStatus = 2;

CREATE UNIQUE INDEX Index_Map_Episode_HellKeep ON Map(EpisodeId)
  WHERE HellKeepWarrensStatus = 1;
