from rest_framework import serializers


class ServerStatusSerializer(serializers.Serializer):
    ServerToken = serializers.CharField()
    Passworded = serializers.BooleanField()
    ServerName = serializers.CharField()
    ForkName = serializers.CharField()
    BuildVersion = serializers.IntegerField()
    CurrentMap = serializers.CharField()
    GameMode = serializers.CharField()
    IngameTime = serializers.CharField()
    RoundTime = serializers.CharField()
    PlayerCount = serializers.IntegerField()
    PlayerCountMax = serializers.IntegerField()
    ServerIP = serializers.CharField()
    ServerPort = serializers.IntegerField()
    WinDownload = serializers.CharField()
    OSXDownload = serializers.CharField()
    LinuxDownload = serializers.CharField()
    fps = serializers.IntegerField()
    GoodFileVersion = serializers.CharField()


class CachedServerStatusSerializer(serializers.Serializer):
    Passworded = serializers.BooleanField()
    ServerName = serializers.CharField()
    ForkName = serializers.CharField()
    BuildVersion = serializers.IntegerField()
    CurrentMap = serializers.CharField()
    GameMode = serializers.CharField()
    IngameTime = serializers.CharField()
    RoundTime = serializers.CharField()
    PlayerCount = serializers.IntegerField()
    PlayerCountMax = serializers.IntegerField()
    ServerIP = serializers.CharField()
    ServerPort = serializers.IntegerField()
    WinDownload = serializers.CharField()
    OSXDownload = serializers.CharField()
    LinuxDownload = serializers.CharField()
    fps = serializers.IntegerField()
    GoodFileVersion = serializers.CharField()


class OwnedBabyServerSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    whitelisted = serializers.BooleanField()
    live = serializers.BooleanField()
    status = CachedServerStatusSerializer(allow_null=True)


class BabyServerTokenSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    serverlist_token = serializers.CharField()
    whitelisted = serializers.BooleanField()


class BabyServerStatusListSerializer(serializers.Serializer):
    servers = CachedServerStatusSerializer(many=True)


class RegenerateServerlistTokenSerializer(serializers.Serializer):
    server_id = serializers.UUIDField()
