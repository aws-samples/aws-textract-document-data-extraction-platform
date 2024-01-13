/**
 * Override CRA configuration without needing to eject.
 *
 * @see https://www.npmjs.com/package/react-app-rewired
 */
module.exports = {
    webpack: function override(config) {
        config.module.rules.push({
            test: /\.(js|mjs|jsx)$/,
            enforce: 'pre',
            loader: require.resolve('source-map-loader'),
            resolve: {
                fullySpecified: false,
            },
        });

        config.resolve.fallback = {
            ...config.resolve.fallback,
            util: false,
        };

        return config;
    },
};
