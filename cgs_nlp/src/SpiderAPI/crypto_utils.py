"""
简单的加密工具类
用于加密存储敏感信息（如 Cookie）
"""

import base64
from cryptography.fernet import Fernet
from django.conf import settings


class SimpleEncryption:
    """
    简单加密工具类
    使用 Django SECRET_KEY 生成加密密钥
    """
    
    @staticmethod
    def get_key():
        """
        获取加密密钥
        从 Django SECRET_KEY 生成 Fernet 密钥
        """
        # 使用 SECRET_KEY 生成一个固定长度的密钥
        secret_key = settings.SECRET_KEY
        
        # 确保密钥长度为 32 字节，然后 base64 编码
        # Fernet 需要一个 URL-safe base64-encoded 32-byte key
        key_bytes = secret_key.encode('utf-8')
        
        # 如果不够 32 字节，填充；如果超过，截断
        key_bytes = key_bytes[:32].ljust(32, b'0')
        
        # 转换为 URL-safe base64
        fernet_key = base64.urlsafe_b64encode(key_bytes)
        return fernet_key
    
    @staticmethod
    def encrypt(text):
        """
        加密文本
        """
        try:
            if not text:
                return text
            
            key = SimpleEncryption.get_key()
            f = Fernet(key)
            encrypted = f.encrypt(text.encode('utf-8'))
            return base64.urlsafe_b64encode(encrypted).decode('utf-8')
        except Exception:
            # 如果加密失败，返回原文（向后兼容）
            return text
    
    @staticmethod
    def decrypt(encrypted_text):
        """
        解密文本
        """
        try:
            if not encrypted_text:
                return encrypted_text
            
            key = SimpleEncryption.get_key()
            f = Fernet(key)
            decoded = base64.urlsafe_b64decode(encrypted_text.encode('utf-8'))
            decrypted = f.decrypt(decoded)
            return decrypted.decode('utf-8')
        except Exception:
            # 如果解密失败，返回原文（向后兼容）
            return encrypted_text

