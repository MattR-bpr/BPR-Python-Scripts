from tkinter import filedialog
from typing import BinaryIO
import utilities


class StreamedDeformationSpecResource:

    def __init__(self, fp: BinaryIO):
        self.mFP = fp


    def Convert(self) -> None:
        # check version
        self.mFP.seek(0x0)
        version = utilities.SwapBytes(self.mFP, "<L")
        assert version == 1, "Bad StreamedDeformationSpecResource version."

        # header
        tag_points_offset = utilities.SwapBytes(self.mFP, "<L")
        tag_points_count = utilities.SwapBytes(self.mFP, "<L")
        driven_points_offset = utilities.SwapBytes(self.mFP, "<L")
        driven_points_count = utilities.SwapBytes(self.mFP, "<L")
        ik_body_parts_offset = utilities.SwapBytes(self.mFP, "<L")
        ik_body_parts_count = utilities.SwapBytes(self.mFP, "<L")
        glass_panes_offset = utilities.SwapBytes(self.mFP, "<L")
        glass_panes_count = utilities.SwapBytes(self.mFP, "<L")
        generic_tags_count = utilities.SwapBytes(self.mFP, "<L")
        generic_tags_offset = utilities.SwapBytes(self.mFP, "<L")
        camera_tags_count = utilities.SwapBytes(self.mFP, "<L")
        camera_tags_offset = utilities.SwapBytes(self.mFP, "<L")
        light_tags_count = utilities.SwapBytes(self.mFP, "<L")
        light_tags_offset = utilities.SwapBytes(self.mFP, "<L")
        self.mFP.seek(0x40)
        self.ConvertVector3()
        for _ in range(4):
            self.ConvertWheelSpec()
        for _ in range(20):
            self.ConvertSensorSpec()
        self.ConvertMatrix4x4()
        self.mFP.seek(0x660)
        for _ in range(5):
            self.ConvertVector3()

        # tag points
        self.mFP.seek(tag_points_offset)
        for _ in range(tag_points_count):
            self.ConvertTagPoint()

        # driven points
        self.mFP.seek(driven_points_offset)
        for _ in range(driven_points_count):
            self.ConvertDrivenPoint()

        # ik body parts
        for i in range(ik_body_parts_count):
            self.ConvertIKBodyPart(ik_body_parts_offset + i * 0x1E0)

        # glass panes
        self.mFP.seek(glass_panes_offset)
        for _ in range(glass_panes_count):
            self.ConvertGlassPane()

        # generic tags
        self.mFP.seek(generic_tags_offset)
        for _ in range(generic_tags_count):
            self.ConvertLocatorPoint()

        # camera tags
        self.mFP.seek(camera_tags_offset)
        for _ in range(camera_tags_count):
            self.ConvertLocatorPoint()

        # light tags
        self.mFP.seek(light_tags_offset)
        for _ in range(light_tags_count):
            self.ConvertLocatorPoint()


    def ConvertVector3(self) -> None:
        # vector 3
        for _ in range(4):
            utilities.SwapBytes(self.mFP, "<L")


    def ConvertMatrix4x4(self) -> None:
        # matrix 4x4
        for _ in range(4):
            self.ConvertVector3()


    def ConvertWheelSpec(self) -> None:
        # wheel spec
        self.ConvertVector3()
        self.ConvertVector3()
        utilities.SwapBytes(self.mFP, "<L")
        self.mFP.seek(0xC, 1)


    def ConvertSensorSpec(self) -> None:
        # sensor spec
        self.ConvertVector3()
        for _ in range(7):
            utilities.SwapBytes(self.mFP, "<L")
        self.mFP.seek(0x14, 1)


    def ConvertTagPoint(self) -> None:
        # tag point
        for _ in range(3):
            self.ConvertVector3()
        for _ in range(3):
            utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<H")
        utilities.SwapBytes(self.mFP, "<H")
        self.mFP.seek(0x10, 1)


    def ConvertDrivenPoint(self) -> None:
        # convert driven point
        self.ConvertVector3()
        utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<H")
        utilities.SwapBytes(self.mFP, "<H")
        self.mFP.seek(0x4, 1)


    def ConvertIKBodyPart(self, ik_body_part_offset: int) -> None:
        # ik body part
        self.mFP.seek(ik_body_part_offset)
        self.ConvertMatrix4x4()
        self.ConvertBodyPartBBox()
        deformation_joints_offset = utilities.SwapBytes(self.mFP, "<L")
        deformation_joints_count = utilities.SwapBytes(self.mFP, "<L")
        for _ in range(6):
            utilities.SwapBytes(self.mFP, "<L")

        # deformation joints
        if deformation_joints_offset != 0:
            self.mFP.seek(deformation_joints_offset)
            for _ in range(deformation_joints_count):
                self.ConvertDeformationJoint()


    def ConvertBodyPartBBox(self) -> None:
        # body part b box
        self.ConvertMatrix4x4()
        for _ in range(10):
            self.ConvertVector3()
            for _ in range(3):
                utilities.SwapBytes(self.mFP, "<L")
            self.mFP.seek(0x4, 1)


    def ConvertDeformationJoint(self) -> None:
        # deformation joint
        for _ in range(3):
            self.ConvertVector3()
        for _ in range(3):
            utilities.SwapBytes(self.mFP, "<L")
        self.mFP.seek(0x4, 1)


    def ConvertGlassPane(self) -> None:
        # glass pane
        for _ in range(5):
            self.ConvertVector3()
        for _ in range(4):
            utilities.SwapBytes(self.mFP, "<H")
        self.mFP.seek(0x4, 1)
        for _ in range(3):
            utilities.SwapBytes(self.mFP, "<H")
        self.mFP.seek(0x2, 1)
        utilities.SwapBytes(self.mFP, "<L")
        self.mFP.seek(0x8, 1)


    def ConvertLocatorPoint(self) -> None:
        # locator point
        self.ConvertMatrix4x4()
        utilities.SwapBytes(self.mFP, "<L")
        utilities.SwapBytes(self.mFP, "<H")
        self.mFP.seek(0xA, 1)


def Main():
    streamed_deformation_spec_resource_path = filedialog.askopenfilename()
    with open(streamed_deformation_spec_resource_path, "r+b") as fp:
        streamed_deformation_spec_resource = StreamedDeformationSpecResource(fp)
        streamed_deformation_spec_resource.Convert()


if __name__ == "__main__":
    Main()