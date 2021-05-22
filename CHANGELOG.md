## [1.1.1](https://github.com/unitystation/unitystation_auth/compare/v1.1.0...v1.1.1) (2021-05-22)


### Bug Fixes

* **account:** fix crash when no badwords.txt file existed ([ba5bd47](https://github.com/unitystation/unitystation_auth/commit/ba5bd4718b00c4db9c7116bf767a80792058c916))

# [1.1.0](https://github.com/unitystation/unitystation_auth/compare/v1.0.0...v1.1.0) (2021-01-11)


### Bug Fixes

* **account:** fix slurs validator triggering when no bad words list has been created ([0620c7a](https://github.com/unitystation/unitystation_auth/commit/0620c7a4beee57c89e009a5f173f40d1ade64ee8))


### Features

* **account:** allow character_settings to be visualized in admin view ([2c09aff](https://github.com/unitystation/unitystation_auth/commit/2c09aff46830cbcf6efaf94376735de56706d3eb))
* **account:** api endpoints to get character data ([ff90616](https://github.com/unitystation/unitystation_auth/commit/ff90616079518f4b900f5e2b0a832be8e9b3bb71))
* **account:** endpoint for token generation ([acbe3d6](https://github.com/unitystation/unitystation_auth/commit/acbe3d6de30be91b7b70640ee79dc8e20bc80ac1))
* **account:** introduce custom validators for username field ([3eb2414](https://github.com/unitystation/unitystation_auth/commit/3eb2414bc6209d32df24e9d0dd35e927e60d7639))
* **account:** make character settings endpoint public ([e360b35](https://github.com/unitystation/unitystation_auth/commit/e360b356083d6cda250eeb111c53fc1097e10327))
* **api:** new register, login, logout and logoutall views ([cea831e](https://github.com/unitystation/unitystation_auth/commit/cea831eba6878092dea709ad7bf7e6f1eae88f9c))

# 1.0.0 (2020-11-22)


### Bug Fixes

* **api:** account register endpoint not requiring mail confirmation ([#11](https://github.com/unitystation/unitystation_auth/issues/11)) ([0044d1f](https://github.com/unitystation/unitystation_auth/commit/0044d1fe303573bb9e13bdf01cc1f4f00bd2eaaf))
* **gha:** fix cache and log in error ([#19](https://github.com/unitystation/unitystation_auth/issues/19)) ([0ea5b16](https://github.com/unitystation/unitystation_auth/commit/0ea5b1608e12026319b155db487f6c9355bce86a))
* **persistence:** correct properties for models ([6ec121b](https://github.com/unitystation/unitystation_auth/commit/6ec121bde5b572b7aa98a6bb0bb98a552a8d40ea))


### Features

* **account:** json field for character settings ([a254169](https://github.com/unitystation/unitystation_auth/commit/a254169c6d49edbf17206534e222efcffbfe92ed))
* **account:** make user_id the model pk ([623d48a](https://github.com/unitystation/unitystation_auth/commit/623d48a8a768a345107a94ffbab17cce28e57ed8))
* **api:** add endpoint to get account data ([fb08042](https://github.com/unitystation/unitystation_auth/commit/fb08042ea54eda092ace21343f503f8376397ff2))
* **api:** set default api views to authenticated only ([4f18737](https://github.com/unitystation/unitystation_auth/commit/4f18737389dc2d39060e33ed9065bcdb58fbd8ed))
* **docker:** enable docker build caching ([#10](https://github.com/unitystation/unitystation_auth/issues/10)) ([3a50d0c](https://github.com/unitystation/unitystation_auth/commit/3a50d0c42f9b3dfce7718d102e16afcc38e5ee0e))
