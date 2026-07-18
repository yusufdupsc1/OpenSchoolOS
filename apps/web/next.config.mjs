/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ["@openschoolos/domain", "@openschoolos/shared", "@openschoolos/ui"],
};

export default nextConfig;
