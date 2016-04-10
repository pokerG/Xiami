DROP TABLE IF EXISTS `song_info`;
CREATE TABLE song_info (
    `SongID` varchar(10) NOT NULL COMMENT '歌曲ID',
    `SongName` varchar(100) NOT NULL COMMENT '歌曲名称',
    `songsterName` varchar(100) NOT NULL COMMENT '歌手',
    `releaseTime` date COMMENT '发布时间',
    PRIMARY KEY (`SongID`),
    KEY `idx_song_songname` (`SongName`),
    KEY `idx_song_songsterName` (`songsterName`),
    KEY `idx_song_releaseTime` (`releaseTime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='歌曲信息表'