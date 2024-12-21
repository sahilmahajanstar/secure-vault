import { Buffer } from 'buffer'

export const generateKey = async (): Promise<CryptoKey> => {
    return await window.crypto.subtle.generateKey(
        {
            name: 'AES-GCM',
            length: 256,
        },
        true, // Extractable
        ['encrypt', 'decrypt'], // Usages
    )
}

export const encryptFile = async (file: File): Promise<string> => {
    const iv = window.crypto.getRandomValues(new Uint8Array(12)) // Initialization vector
    // it is 8 bit array that is element upto 2^8 = 256
    // 12 length means 12 * 8 = 96 bit = 12 bytes
    // hex char represent 4 bit = 2^4 = 16
    // so 12 bytes = 12 * 8 = 96 bit = 96 / 4 = 24 hex char
    const fileData = await file.arrayBuffer() // Read file as ArrayBuffer
    const key = await generateKey()
    const exported = await window.crypto.subtle.exportKey('raw', key)
    const encryptedData = await window.crypto.subtle.encrypt(
        {
            name: 'AES-GCM',
            iv: iv,
        },
        key,
        fileData,
    )
    const result = {
        iv: Buffer.from(iv).toString('hex'),
        encryptedData: Buffer.from(encryptedData).toString('hex'),
        key: Buffer.from(exported).toString('hex'),
    }
    return result.key + '@' + result.iv + result.encryptedData
}

export const decryptFile = async (encryptedData: string): Promise<Blob> => {
    const [key, encrypt] = encryptedData.split('@')
    const iv = Uint8Array.from(Buffer.from(encrypt.slice(0, 24), 'hex'))
    const webKey = await window.crypto.subtle.importKey(
        'raw',
        Uint8Array.from(Buffer.from(key, 'hex')),
        {
            name: 'AES-GCM',
            length: 256,
        },
        true, // Extractable
        ['encrypt', 'decrypt'], // Usages
    )
    const decryptedData = await window.crypto.subtle.decrypt(
        {
            name: 'AES-GCM',
            iv: iv,
        },
        webKey,
        Uint8Array.from(Buffer.from(encrypt.slice(24), 'hex')),
    )
    return new Blob([decryptedData]) // Return as Blob
}
