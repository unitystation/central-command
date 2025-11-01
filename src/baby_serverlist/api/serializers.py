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


class ActiveServersSerializer(serializers.Serializer):
    CashDateTime = serializers.DateTimeField()
    servers = ServerStatusSerializer(many=True)


class RegenerateServerlistTokenSerializer(serializers.Serializer):
    server_id = serializers.UUIDField()
