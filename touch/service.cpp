/*
 * Copyright (C) 2020-2026 The LineageOS Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#define LOG_TAG "vendor.lineage.touch-service.lge_sm8150"

#include <android-base/logging.h>
#include <android/binder_manager.h>
#include <android/binder_process.h>

#include "GloveMode.h"
#include "TouchscreenGesture.h"

using aidl::vendor::lineage::touch::GloveMode;
using aidl::vendor::lineage::touch::TouchscreenGesture;

int main() {
    ABinderProcess_setThreadPoolMaxThreadCount(0);

    std::shared_ptr<GloveMode> gloveMode = ndk::SharedRefBase::make<GloveMode>();
    std::shared_ptr<TouchscreenGesture> touchscreenGesture =
            ndk::SharedRefBase::make<TouchscreenGesture>();

    const std::string gloveModeInstance = std::string(GloveMode::descriptor) + "/default";
    binder_status_t status =
            AServiceManager_addService(gloveMode->asBinder().get(), gloveModeInstance.c_str());
    CHECK_EQ(status, STATUS_OK) << "Failed to add service " << gloveModeInstance << " " << status;

    const std::string gestureInstance =
            std::string(TouchscreenGesture::descriptor) + "/default";
    status = AServiceManager_addService(touchscreenGesture->asBinder().get(),
                                        gestureInstance.c_str());
    CHECK_EQ(status, STATUS_OK) << "Failed to add service " << gestureInstance << " " << status;

    ABinderProcess_joinThreadPool();
    return EXIT_FAILURE;  // should not reach
}
