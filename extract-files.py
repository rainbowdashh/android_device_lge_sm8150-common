#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.file import File
from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    "hardware/lge",
    "hardware/qcom-caf/common/libqti-perfd-client",
    "hardware/qcom-caf/sm8150",
    "hardware/qcom-caf/wlan",
    "vendor/qcom/opensource/commonsys/display",
    "vendor/qcom/opensource/dataservices",
    "vendor/qcom/opensource/display",
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'vendor.qti.hardware.fm@1.0',
        'vendor.qti.hardware.qteeconnector@1.0',
        'vendor.qti.imsrtpservice@3.0',
    ): lib_fixup_vendor_suffix,
    'libwpa_client': lib_fixup_remove,
}


blob_fixups: blob_fixups_user_type = {
    'vendor/etc/init/vendor.sensors.sscrpcd.rc': blob_fixup()
        .regex_replace('class early_hal', 'class core'),
    'vendor/lib64/vendor.lge.hardware.powerhint.rescontrol@2.0-common.so': blob_fixup()
        # Preserve x24/x25 across the broken per-app XML constructor. Its
        # missing-file path violates the arm64 ABI and corrupts linker state.
        .sig_replace(
            'FD 7B BE A9 F3 0B 00 F9 FD 03 00 91 53 00 00 B0 '
            '73 96 42 F9 41 01 80 52 E0 03 13 AA 3C 20 00 94 '
            'E1 03 13 AA F3 0B 40 F9 E0 FF FF F0 42 00 00 B0 '
            '00 20 2E 91 42 00 00 91 FD 7B C2 A8 38 20 00 14',
            'FD 7B BD A9 F3 63 01 A9 F9 13 00 F9 53 00 00 B0 '
            '73 96 42 F9 41 01 80 52 E0 03 13 AA 3C 20 00 94 '
            'E1 03 13 AA F3 63 41 A9 F9 13 40 F9 40 D1 FF 10 '
            'E2 74 04 10 FD 7B 40 A9 FF C3 00 91 38 20 00 14',
        ),
    ('vendor/lib/libwvhidl.so', 'vendor/lib64/libwvhidl.so'): blob_fixup()
        .add_needed('libcrypto_shim.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'sm8150-common',
    'lge',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
