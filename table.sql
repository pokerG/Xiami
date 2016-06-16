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

DROP TABLE IF EXISTS `roomtrasnfer`
CREATE TABLE roomtrasnfer (
    `ShopRoomSortID` int(11) NOT NULL,
    `CompanyID` int(11) NOT NULL,
    `RoomSortID` int(11) NOT NULL,
    `RoomSortName` varchar(100) NOT NULL,
    `size` varchar(10) NOT NULL,
    `topic` varchar(10) NOT NULL,
    `serve` varchar(10) NOT NULL,
    PRIMARY KEY (`ShopRoomSortID`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8


DROP TABLE IF EXISTS `materialtrasnfer`
CREATE TABLE materialtrasnfer (
    `ShopMaterialSortID` int(11) NOT NULL,
    `CompanyID` int(11) NOT NULL,
    `SerialNumber` int(11) NOT NULL,
    `MaterialSortID` int(11) NOT NULL,
    `MaterialSortName` varchar(100) NOT NULL,
    `MaterialClass` varchar(10) NOT NULL,
    PRIMARY KEY (`ShopMaterialSortID`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8
