import type { NextConfig } from 'next';

const config: NextConfig = {
  reactStrictMode: true,

  /** 워크스페이스 패키지는 소스를 그대로 내보내므로 Next 가 트랜스파일하게 한다. */
  transpilePackages: ['@echoa/api', '@echoa/core', '@echoa/db'],

  typedRoutes: true,
};

export default config;
