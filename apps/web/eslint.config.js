import baseConfig from '@echoa/eslint-config/base';
import nextConfig from '@echoa/eslint-config/nextjs';

export default [...baseConfig, ...nextConfig, { ignores: ['.next/**'] }];
