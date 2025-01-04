// Generate a secure API key
export function generateApiKey(): string {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  const prefix = 'reapi';
  const randomPart = Array.from(
    { length: 32 },
    () => chars.charAt(Math.floor(Math.random() * chars.length))
  ).join('');
  
  return `${prefix}_${randomPart}`;
}